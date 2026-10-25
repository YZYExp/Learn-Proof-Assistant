namespace Book

theorem swapAnd (P Q : Prop) : P ∧ Q → Q ∧ P := by
  intro h
  constructor
  · exact h.right
  · exact h.left

theorem passAlong (P Q : Prop) : (P → Q) → P → Q := by
  intro f hp
  exact f hp

theorem existsSelf : ∃ n : Nat, n = n := by
  exact ⟨0, rfl⟩

theorem replaceArg (f : Nat → Nat) (a b : Nat) (h : a = b) : f a = f b := by
  rw [h]

def addLeft : Nat → Nat → Nat
  | 0, m => m
  | Nat.succ n, m => Nat.succ (addLeft n m)

theorem addLeft_zero (n : Nat) : addLeft n 0 = n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change Nat.succ (addLeft n 0) = Nat.succ n
      rw [ih]

def join {α : Type} : List α → List α → List α
  | [], ys => ys
  | x :: xs, ys => x :: join xs ys

def count {α : Type} : List α → Nat
  | [] => 0
  | _ :: xs => Nat.succ (count xs)

theorem count_join {α : Type} (xs ys : List α) :
    count (join xs ys) = count xs + count ys := by
  induction xs with
  | nil => simp [join, count]
  | cons x xs ih => simp [join, count, ih, Nat.succ_add]

def reverseSlow {α : Type} : List α → List α
  | [] => []
  | x :: xs => join (reverseSlow xs) [x]

end Book
