;; demonstrate usage of comp(composistion)
(def negated (comp - +))
(println (nagated 1 4 56.9))

;; focus on results, not steps
(println (reduce + (map #(* 2 %) (filter odd? (range 1 20)))))

