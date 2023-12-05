-------------- MODULE DeviceModel --------------

EXTENDS Integers, Sequences, TLC

CONSTANTS MaxValue

VARIABLE state

Init ==
    /\ state \in {0, 1}  \* Assuming a binary state: 0 for off, 1 for on

On ==
    /\ state = 0
    /\ state' = 1

Off ==
    /\ state = 1
    /\ state' = 0

Toggle ==
    \/ On
    \/ Off

Next ==
    \/ Toggle

Spec == Init /\ [][Next]_<<state>>

=============================================
