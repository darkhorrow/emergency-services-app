
; auxiliar functions
(deffunction ceil(?value)
  (bind ?x (mod ?value 1))
  (if (> ?x 0) then
      (+ (integer ?value) 1)
    else
      (integer ?value)
  )
)

(deffunction truncate(?value ?digits)
  (bind ?exp (** 10 ?digits))
  (bind ?x (* ?value ?exp))
  (bind ?x (integer ?x))
  (/ ?x ?exp)
)

; templates
(deftemplate Service
  (slot id (type INTEGER))
  (slot name (allowed-values Sanitary Firemen Policemen))
  (multislot location (type FLOAT)); km
  (slot n_members (type INTEGER))
  (slot movement_speed (type FLOAT)); km/h
  (slot prep_time (type FLOAT)) ; h
)

(deftemplate Emergency
  (slot id (type INTEGER))
  (slot type (allowed-values natural_disaster thief homicide pandemic car_crash))
  (multislot location (type FLOAT)) ; km
  (slot n_affected_people (type INTEGER))
)

(defrule notifyExistenceService
  (Service (name ?name) (location ?loc_X ?loc_Y))
  =>
  (printout t "Service " ?name " situated at (" ?loc_X " " ?loc_Y ") ready!" crlf)
)

(defrule emergencySpotted
  ?e <- (Emergency (id ?id) (type ?type) (location ?loc_X ?loc_Y) (n_affected_people ?n_affected))
  =>
  (printout t "A emergency appeared!" crlf)
  (assert
    (choose-service ?id ?type ?n_affected ?loc_X ?loc_Y)
  )
)

; Emergency type handler

(defrule is-thief
  ?serv <- (choose-service ?id ?type ?n_affected ?x ?y)
  (test (eq ?type thief))
  =>
  (printout t "Is a thief emergency" crlf)
  ; calculate required staff: 1 member/10 people
  (bind ?staff (ceil (/ ?n_affected 10)))
  (assert
    (call Policemen ?id ?x ?y ?staff)
  )
  ; delete choose-service
  (retract ?serv)
)

(defrule is-natural_disaster
  ?serv <- (choose-service ?id ?type ?n_affected ?x ?y)
  (test (eq ?type natural_disaster))
  =>
  (printout t "Is a natural desaster emergency" crlf)
  ; calculate required staff: 1 member/10 people
  (bind ?staff (ceil (/ ?n_affected 10)))
  (assert
    (call Policemen ?id ?x ?y ?staff)
  )
  (assert
    (call Sanitary ?id ?x ?y ?staff)
  )
  (assert
    (call Firemen ?id ?x ?y ?staff)
  )
  ; delete choose-service
  (retract ?serv)
)

(defrule is-homicide
  ?serv <- (choose-service ?id ?type ?n_affected ?x ?y)
  (test (eq ?type homicide))
  =>
  (printout t "Is a homicide emergency" crlf)
  ; calculate required staff: 1 member/10 people
  (bind ?staff (ceil (/ ?n_affected 10)))
  (assert
    (call Policemen ?id ?x ?y ?staff)
  )
  (assert
    (call Sanitary ?id ?x ?y ?staff)
  )
  ; delete choose-service
  (retract ?serv)
)

(defrule is-pandemic
  ?serv <- (choose-service ?id ?type ?n_affected ?x ?y)
  (test (eq ?type pandemic))
  =>
  (printout t "Is a pandemic emergency" crlf)
  ; calculate required staff: 1 member/10 people
  (bind ?staff (ceil (/ ?n_affected 10)))
  (assert
    (call Sanitary ?id ?x ?y ?staff)
  )
  ; delete choose-service
  (retract ?serv)
)

(defrule is-car-crash
  ?serv <- (choose-service ?id ?type ?n_affected ?x ?y)
  (test (eq ?type car_crash))
  =>
  (printout t "Is a car crash emergency" crlf)
  ; calculate required staff: 1 member/10 people
  (bind ?staff (ceil (/ ?n_affected 10)))
  (assert
    (call Policemen ?id ?x ?y ?staff)
  )
  (assert
    (call Firemen ?id ?x ?y ?staff)
  )
  ; delete choose-service
  (retract ?serv)
)

; Service calls

(defrule select-station
  ?call <- (call ?name ?emergency_id ?x ?y ?staff)
  =>
  (do-for-all-facts ((?service Service)) TRUE
    (if (eq ?service:name ?name)
     then
      (bind ?id ?service:id)
      (bind ?locx (nth$ 1 (fact-slot-value ?service location)))
      (bind ?locy (nth$ 2 (fact-slot-value ?service location)))
      (bind ?dist (sqrt (+ (* (- ?x ?locx) (- ?x ?locx)) (* (- ?y ?locy) (- ?y ?locy)))) )
      (bind ?mov_time (/ ?dist ?service:movement_speed))
      (bind ?time (+ ?mov_time ?service:prep_time))
      (assert (distance-station ?name ?emergency_id ?service:id ?time ?staff))
    )
  )
  (retract ?call)
)

(defrule attend-emergency
  ?ds <- (distance-station ?type ?emergency_id ?service_id ?time ?staff)
  ?service <- (Service (id ?id_service) (n_members ?n_members))
  (forall (and (distance-station ?emer_id ?serv_id ?ds_time ?s)
               (Service (id ?serv_id) (n_members ?n_mem))
          )
          (test (<= ?time ?ds_time))
  )
  (test (eq ?id_service ?service_id))
  =>
  (retract ?ds)
  ; eliminar staff del servicio
  (bind ?resto (- ?staff ?n_members)); numero de miembros restantes que hacen falta
  (bind ?new_n_members 0)
  (if (>= ?resto 0)
   then
      (bind ?new_n_members 0)
   else
      (bind ?resto 0)
      (bind ?new_n_members (- ?n_members ?staff))
  )
  (modify ?service (n_members ?new_n_members))
  ; actualizar todos los distance-station
  (do-for-all-facts ((?distance_station distance-station)) TRUE
    (bind ?tipo (nth$ 1 (fact-slot-value ?distance_station implied)) )
    (bind ?emergencia_id (nth$ 2 (fact-slot-value ?distance_station implied)) )
    (bind ?servicio_id (nth$ 3 (fact-slot-value ?distance_station implied)) )
    (bind ?tiempo (nth$ 4 (fact-slot-value ?distance_station implied)) )
    (bind ?staff (nth$ 5 (fact-slot-value ?distance_station implied)) )
    (if (and
          (eq ?tipo ?type)
          (eq ?emergencia_id ?emergency_id)
        )
     then
      (retract ?distance_station)
      (assert (distance-station ?tipo ?emergencia_id ?servicio_id ?tiempo ?resto))
    )
  )

  (printout t "Emergency [" ?emergency_id "] " ?type " station [" ?service_id "] time " ?time " -- " ?staff crlf)
)

(defrule finish-emergency-service
  ?end_service <- (end-service ?id ?staff)
  ?serv <- (Service (id ?id_serv) (name ?serv_name) (location ?loc_X ?loc_Y) (n_members ?members) (movement_speed ?speed) (prep_time ?time))
  (test (eq ?id ?id_serv))
  =>
  (retract ?serv)
  (assert
    (Service
      (id ?id)
      (name ?serv_name)
      (location ?loc_X ?loc_Y)
      (n_members (+ ?members ?staff))
      (movement_speed ?speed)
      (prep_time ?time)
    )
  )
  (retract ?end_service)
)