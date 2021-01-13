% rebase('base.tpl', title='Server Login')
<div class="container position-absolute top-50 start-50 translate-middle bg-dark"
     style="max-width: 512px; padding:20px; border-radius: 10px; border: 1px solid silver">
  <h1 class="text-center">천국의 문 v2.10.6</h1>
  <p class="text-center">시스템에 액세스하려면, 로그인 해주세요.</p>

  <form id="login" action="/login" method="post">
    <label for="username" class="form-label">사용자 이름: </label>
    <div class="input-group mb-3">
      <span class="input-group-text"><i class="bi-person-circle"></i></span>
      <input type="input" class="form-control" id="username-input" name="username" />
    </div>
    <label for="password" class="form-label">암호: </label>
    <div class="input-group mb-3">
      <span class="input-group-text"><i class="bi-key"></i></span>
      <input type="password" class="form-control" id="password-input" name="password" />
    </div>
    <button class="btn btn-primary" type="submit">로그인<i class="bi-box-arrow-in-right"></i></button>
  </form>
</div>

<script>
  $(document).ready(function() {
    // Clear data of previous logins
    window.localStorage.clear();
    // Clear local storage
    $('#login').submit(function(result) {
      if (!$('#username-input').val()) {
        alert('Missing username.');
        return false;
      }
      if (!$('#password-input').val()) {
        alert('Missing password.');
        return false;
      }

    });
  });
</script>
