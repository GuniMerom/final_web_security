<!DOCTYPE html>
<html>
  <head>
    <title>Server Login</title>
    <meta charset="utf-8" />
  <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
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

	 // window.location.href = "/";

          //window.location.replace("127.0.0.1:8000/");
        });
      });
    </script>
  </head>
  <body>
    <div class="container">
      <h1>Attackers management server <br><small>Россия, вперёд!</small></h1>
      <p>To access the management, please log in.</p>
      <form id="login" action="/login" method="post">
        <div class="form-group">
          <label for="username">Username: </label>
          <input type="input" class="form-control" id="username-input" name="username" />
        </div>
        <div class="form-group">
          <label for="password">Password: </label>
          <input type="password" class="form-control" id="password-input" name="password" />
        </div>

	<input type="submit"  value="Submit request">
        <!-- <button type="submit" onclick="window.location.href = '/' class="btn btn-default">Submit</button> -->
      </form>
    </div>
  </body>
</html>
