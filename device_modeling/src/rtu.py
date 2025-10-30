# A simple RTU (outstation) that does:
#   - N CircuitBreaker devices
#   - 1 Disconnector device
#   - 1 PowerTransformer (voltage) + 1 CurrentTransformer (current) for measurements
#
# DNP3 point contract (freeze these indices once wired):
#   Binary Inputs (BI — Group 1 Var 2)
#     For each breaker i:
#       BI[breakerClosed[i]]  True when breaker i is CLOSED, False when OPEN
#       UPDATE: write after any state change and on each scan (edge-detected events)
#     Disconnector:
#       BI[discClosed]       True when disconnector is CLOSED
#       UPDATE: after any state change and on each scan (edge-detected)
#
#   Analog Inputs (AI — Group 30 Var 5, float)
#     AI[0] feederAmps  (A)    From CurrentTransformer secondary current
#       UPDATE: each scan; deadband (default 0.5 A)
#     AI[1] busKV       (kV)   From PowerTransformer secondary voltage (convert to kV)
#       UPDATE: each scan; deadband (default 0.02 kV)
#     AI[2] xfmrKW      (kW)   Derived: busKV * feederAmps * power_factor
#       UPDATE: each scan; deadband (default 5.0 kW)
#
#   Binary Outputs (BO — Group 12 Var 1, latch)
#     For each breaker i:  BO[ breakerCmd[i] ]  1=CLOSE, 0=OPEN (trip)
#       SELECT: allow only 0/1
#       OPERATE: value==1 -> breaker.close(); value==0 -> breaker.open()
#                then reflect to BI[breakerClosed[i]]
#     Disconnector:        BO[ discCmd ]       1=CLOSE, 0=OPEN
#       SELECT/OPERATE: same pattern; reflect to BI[discClosed]
#
# Recommended classes:
#   - BI[*]  -> Class 1 (events on change)
#   - AI[*]  -> Class 2 (deadbanded analog events)

import time
import threading



class AnalogPoint(object):
    def __init__(self):
        self.value = 0.0
        self.deadband = 0.0
        self.last_event_value = 0.0


class BinaryPoint(object):
    def __init__(self):
        self.value = False


class RTUDB(object):
    def __init__(self):
        self.ai = {}      # index -> AnalogPoint
        self.bi = {}      # index -> BinaryPoint
        self.events = []  # list of tuples: (AI/BI, index, value, timestamp)
        self._lock = threading.RLock()

    def set_ai(self, index, new_value, deadband=None):
        with self._lock:
            if index not in self.ai:
                self.ai[index] = AnalogPoint()
            pt = self.ai[index]
            if deadband is not None:
                pt.deadband = float(deadband)

            newf = float(new_value)
            if abs(newf - pt.last_event_value) >= float(pt.deadband):
                pt.value = newf
                pt.last_event_value = newf
                self.events.append(("AI", int(index), newf, float(time.time())))
            else:
                pt.value = newf  # snapshot only

    def set_bi(self, index, new_value):
        with self._lock:
            if index not in self.bi:
                self.bi[index] = BinaryPoint()
            prev = bool(self.bi[index].value)
            newb = bool(new_value)
            if prev != newb:
                self.bi[index].value = newb
                self.events.append(("BI", int(index), newb, float(time.time())))
            else:
                self.bi[index].value = newb  # keep snapshot consistent

    def drain_events(self, max_events=256):
        with self._lock:
            if max_events <= 0 or max_events >= len(self.events):
                out = list(self.events)
                self.events = []
                return out
            out = self.events[:max_events]
            self.events = self.events[max_events:]
            return out


class TransformerMeasAdapter(object):
    
    #Adapter that reads PowerTransformer + CurrentTransformer objects
    def __init__(self, power_tx, current_tx, power_factor=1.0, volts_to_kv=0.001):
        self.power_tx = power_tx # PowerTransformer (voltage src)
        self.current_tx = current_tx # CurrentTransformer (current src)
        self.power_factor = float(power_factor) # used for kW derivation (default 1)
        self.volts_to_kv = float(volts_to_kv) # scale if voltage is in volts

    def _read_voltage_kv(self):
        if hasattr(self.power_tx, "get_secondary_voltage"):
            v = self.power_tx.get_secondary_voltage()
        elif hasattr(self.power_tx, "get_output_voltage"):
            v = self.power_tx.get_output_voltage()
        elif hasattr(self.power_tx, "get_primary_voltage"):
            v = self.power_tx.get_primary_voltage()
        else:
            v = 0.0
        return float(v) * self.volts_to_kv #conversion

    def _read_current_amps(self):
        if hasattr(self.current_tx, "get_secondary_current"):
            i = self.current_tx.get_secondary_current()
        elif hasattr(self.current_tx, "get_output_current"):
            i = self.current_tx.get_output_current()
        elif hasattr(self.current_tx, "get_primary_current"):
            i = self.current_tx.get_primary_current()
        else:
            i = 0.0
        return float(i)

    def sample(self):
        amps = self._read_current_amps()
        kv = self._read_voltage_kv()
        kw = kv * amps * self.power_factor
        return (amps, kv, kw)


class RTU(object):
    """
    RTU (outstation) that fronts:
      - breakers: list of CircuitBreaker (expects .is_closed, .open(), .close())
      - disconnector: expects .closed bool, .open(), .close()
      - meas_adapter: TransformerMeasAdapter that provides (amps, kV, kW)

    DNP3 glue:
      - READS: use rtu.point_map (BI/AI indices)
      - COMMANDS: call rtu.select_bo(index, value) then rtu.operate_bo(index, value)
      - SCAN: call rtu.scan_once(); serve events via rtu.db.drain_events()
    """

    # Fixed AI indices (freeze for outstation config)
    AI_FEEDER_AMPS = 0
    AI_BUS_KV = 1
    AI_XFMR_KW = 2

    def __init__(self,
                 breakers,
                 disconnector,
                 meas_adapter,
                 ai_deadband_amps=0.5,
                 ai_deadband_kv=0.02,
                 ai_deadband_kw=5.0):
        self.db = RTUDB()
        self.breakers = breakers
        self.disc = disconnector
        self.meas = meas_adapter

        self.ai_deadband_amps = float(ai_deadband_amps)
        self.ai_deadband_kv = float(ai_deadband_kv)
        self.ai_deadband_kw = float(ai_deadband_kw)

        
        # BI map: breakerClosed[i] = i
        self.BI_breakerClosed = {}
        i = 0
        while i < len(self.breakers):
            self.BI_breakerClosed[i] = i
            i += 1
        # disconnector BI right after breakers
        self.BI_discClosed = len(self.breakers)

        # BO map: breakerCmd[i] = i
        self.BO_breakerCmd = {}
        j = 0
        while j < len(self.breakers):
            self.BO_breakerCmd[j] = j
            j += 1
        # disconnector BO right after breakers
        self.BO_discCmd = len(self.breakers)

        # Public point map for wiring/logging
        self.point_map = {"BI": {}, "AI": {}, "BO": {}}
        k = 0
        while k < len(self.breakers):
            self.point_map["BI"]["breakerClosed[" + str(k) + "]"] = self.BI_breakerClosed[k]
            k += 1
        self.point_map["BI"]["discClosed"] = self.BI_discClosed

        self.point_map["AI"]["feederAmps"] = self.AI_FEEDER_AMPS
        self.point_map["AI"]["busKV"] = self.AI_BUS_KV
        self.point_map["AI"]["xfmrKW"] = self.AI_XFMR_KW

        m = 0
        while m < len(self.breakers):
            self.point_map["BO"]["breakerCmd[" + str(m) + "]"] = self.BO_breakerCmd[m]
            m += 1
        self.point_map["BO"]["discCmd"] = self.BO_discCmd

        # Seed initial BI snapshot (so integrity polls return something)
        n = 0
        while n < len(self.breakers):
            brk = self.breakers[n]
            is_closed_value = False
            if hasattr(brk, "is_closed"):
                is_closed_value = bool(brk.is_closed)
            self.db.set_bi(self.BI_breakerClosed[n], is_closed_value)
            n += 1

        disc_closed_value = False
        if hasattr(self.disc, "closed"):
            disc_closed_value = bool(self.disc.closed)
        self.db.set_bi(self.BI_discClosed, disc_closed_value)

  
    def scan_once(self):
        """
        Call periodically. Updates:
          - AI[0,1,2]: deadbanded from meas_adapter.sample()
          - BI[*]: edge-detected snapshots from device states
        """
        amps = 0.0
        kv = 0.0
        kw = 0.0
        sample_tuple = self.meas.sample()
        if isinstance(sample_tuple, tuple) and len(sample_tuple) == 3:
            amps = float(sample_tuple[0])
            kv = float(sample_tuple[1])
            kw = float(sample_tuple[2])

        self.db.set_ai(self.AI_FEEDER_AMPS, amps, deadband=self.ai_deadband_amps)
        self.db.set_ai(self.AI_BUS_KV, kv, deadband=self.ai_deadband_kv)
        self.db.set_ai(self.AI_XFMR_KW, kw, deadband=self.ai_deadband_kw)

        i = 0
        while i < len(self.breakers):
            brk = self.breakers[i]
            is_closed_value = False
            if hasattr(brk, "is_closed"):
                is_closed_value = bool(brk.is_closed)
            self.db.set_bi(self.BI_breakerClosed[i], is_closed_value)
            i += 1

        disc_closed_value = False
        if hasattr(self.disc, "closed"):
            disc_closed_value = bool(self.disc.closed)
        self.db.set_bi(self.BI_discClosed, disc_closed_value)

   
    def select_bo(self, index, value):
        """
        Validate a Group12Var1 latch command (0 or 1).
        Returns (ok: bool, msg: str).
        """
        if value not in (0, 1):
            return (False, "BAD_VALUE")

        # Breaker command?
        for breaker_number, mapped_index in self.BO_breakerCmd.items():
            if index == mapped_index:
                return (True, "OK")

        # Disconnector command?
        if index == self.BO_discCmd:
            return (True, "OK")

        return (False, "UNKNOWN_INDEX")

    def operate_bo(self, index, value):
        """
        Apply Group12Var1 latch command:
          - breakerCmd[i]: 1=CLOSE, 0=OPEN
          - discCmd:       1=CLOSE, 0=OPEN
        Reflect results to BI immediately.
        Returns (ok: bool, msg: str).
        """
        # Breaker?
        for breaker_number, mapped_index in self.BO_breakerCmd.items():
            if index == mapped_index:
                brk = self.breakers[breaker_number]
                if value == 1:
                    if hasattr(brk, "close"):
                        brk.close()
                    self.db.set_bi(self.BI_breakerClosed[breaker_number], True)
                else:
                    if hasattr(brk, "open"):
                        brk.open()
                    self.db.set_bi(self.BI_breakerClosed[breaker_number], False)
                return (True, "OK")

        # Disconnector?
        if index == self.BO_discCmd:
            if value == 1:
                if hasattr(self.disc, "close"):
                    self.disc.close()
                self.db.set_bi(self.BI_discClosed, True)
            else:
                if hasattr(self.disc, "open"):
                    self.disc.open()
                self.db.set_bi(self.BI_discClosed, False)
            return (True, "OK")

        return (False, "UNKNOWN_INDEX")
