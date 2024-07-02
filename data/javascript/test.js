function factorial(n) {
  /**
   * This function perform a factorial (n!) of the number n provided in the argument
   */
  if (n === 0 || n === 1) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}
