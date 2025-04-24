# 🧮 Computor v1

_"I’m not a graduate either."_  
This project is your first step into the mathematical world of 42's ecosystem — rebuilding algebra skills from scratch and learning how to solve polynomial equations by coding them yourself.

> 🛠️ This project was fully implemented by **Me**.

---

## 🎯 Project Goal

To write a program that solves polynomial equations up to the **second degree**. The project aims to:

- Refresh your math fundamentals (equations, polynomials, roots, discriminants).
- Help you understand how these concepts are used in more advanced projects.
- Encourage you to manipulate math expressions **manually** (no math libraries for shortcuts!).

---

## 💡 Key Features

Your `computor` program should:

- ✅ Reduce any polynomial equation to its simplified form.
- ✅ Determine and print the degree of the polynomial.
- ✅ Solve equations up to degree 2:
  - Linear equations (degree 1)
  - Quadratic equations (degree 2)
  - Identify discriminant sign (positive, zero, negative)
- ✅ Handle special cases like:
  - No solution
  - Infinite solutions
  - Invalid polynomial degree (>2)

---

## 🧪 Example Usage

```bash
$> ./computor "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
0.905239
-0.475131

$> ./computor "5 * X^0 + 4 * X^1 = 4 * X^0"
Reduced form: 1 * X^0 + 4 * X^1 = 0
Polynomial degree: 1
The solution is:
-0.25
