;: Replacing this with add-hook 'org-mode in .spacemacs
;; (
;;  (org-mode
;;   (eval
;;    .
;;    (progn
;;      ;; info:org#Conflicts for org 9 and very recent yas
;;      (defun yas/org-very-safe-expand ()
;;        (let ((yas/fallback-behavior 'return-nil)) (yas/expand)))

;;      (yas/expand)
;;      (make-variable-buffer-local 'yas/trigger-key)
;;      (setq yas/trigger-key [tab])
;;      (add-to-list 'org-tab-first-hook 'yas/org-very-safe-expand)
;;      (define-key yas/keymap [tab] 'yas/next-field)
;;      )
;;    )
;;   )
;;  )
