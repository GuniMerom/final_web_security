<!DOCTYPE html>
<html>
  <head>
    <title>Server Login</title>
    <meta charset="utf-8" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>$(document).ready(function() { $('body').bootstrapMaterialDesign(); });</script>

    <link rel="stylesheet" href="/static/custom.css">
    <script>
      $(document).ready(function() {
        // Clear data of previous logins
        window.localStorage.clear();
        // Clear local storage
        $('#login').submit(function(result) {
          if (!$('#username-input').val()) {
            alert('Please insert a username.');
            return false;
          }
          if (!$('#password-input').val()) {
            alert('Please insert a password.');
            return false;
          }

        });
      });
    </script>
  </head>
  <body>
    <div class="container position-absolute top-50 start-50 translate-middle" style="max-width: 512px">
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
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
  </body>
</html>
