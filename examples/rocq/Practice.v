From Stdlib Require Import Lists.List.
Import ListNotations.

Module Book.

Theorem swap_and : forall P Q : Prop, P /\ Q -> Q /\ P.
Proof.
  intros P Q h.
  destruct h as [hp hq].
  split.
  - exact hq.
  - exact hp.
Qed.

Theorem pass_along : forall P Q : Prop, (P -> Q) -> P -> Q.
Proof.
  intros P Q f hp.
  exact (f hp).
Qed.

Theorem exists_self : exists n : nat, n = n.
Proof.
  exists 0.
  reflexivity.
Qed.

Theorem replace_arg : forall (f : nat -> nat) (a b : nat),
  a = b -> f a = f b.
Proof.
  intros f a b h.
  rewrite h.
  reflexivity.
Qed.

Fixpoint add_left (n m : nat) : nat :=
  match n with
  | O => m
  | S k => S (add_left k m)
  end.

Theorem add_left_zero : forall n : nat, add_left n 0 = n.
Proof.
  intro n.
  induction n as [| k ih].
  - reflexivity.
  - simpl.
    rewrite ih.
    reflexivity.
Qed.

Fixpoint join {A : Type} (xs ys : list A) : list A :=
  match xs with
  | [] => ys
  | x :: rest => x :: join rest ys
  end.

Fixpoint count {A : Type} (xs : list A) : nat :=
  match xs with
  | [] => O
  | _ :: rest => S (count rest)
  end.

Theorem count_join : forall (A : Type) (xs ys : list A),
  count (join xs ys) = count xs + count ys.
Proof.
  intros A xs ys.
  induction xs as [| x rest ih].
  - reflexivity.
  - simpl.
    rewrite ih.
    reflexivity.
Qed.

Fixpoint reverse_slow {A : Type} (xs : list A) : list A :=
  match xs with
  | [] => []
  | x :: rest => join (reverse_slow rest) [x]
  end.

End Book.
