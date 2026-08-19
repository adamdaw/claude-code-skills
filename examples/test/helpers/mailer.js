// A test double, deliberately outside src/ so the mutation run does not mutate
// it. Only the code under test gets mutated.
export class Mailer {
  #sent = 0;

  send(message) {
    this.#sent += 1;
    return message;
  }

  sentCount() {
    return this.#sent;
  }
}
