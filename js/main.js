const $loginForm = $("#login-form");
const $signupForm = $("#signup-form");
const $loginBtn = $("#login-button");
const $signupBtn = $("#signup-button");
const $graphs1 = $("#graphs1");
const $graphs2 = $("#graphs2");
const $welcome = $("#welcome");
const $logoutBtn = $("#logout-button");
const $userBtn = $("#user-button");
const $goodbye = $("#goodbye");
const $teamsMain1 = $("#teams-main1");
const $teamsMain2 = $("#teams-main2");
const $teamName1 = $("#team-name1");
const $teamName2 = $("#team-name2");

function hidePageComponents() {
  const components = [
    $loginForm,
    $signupForm,
    $loginBtn,
    $signupBtn,
    $graphs1,
    $graphs2,
    $welcome,
    $logoutBtn,
    $userBtn,
    $goodbye,
  ];
  components.forEach((c) => c.hide());
}
