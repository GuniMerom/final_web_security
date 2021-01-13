<!DOCTYPE html>
<html>
  <head>
    <title>{{title or 'Untitled'}}</title>
    <meta charset="utf-8" />
    % if get('offline', True):
    <link href="/static/bootstrap-5.0.0-beta1/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/bootstrap-icons-1.3.0/bootstrap-icons.css">
    <script src="/static/jquery-3.2.1/jquery-3.2.1.slim.min.js"></script>
    % else:
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    % end
    <link rel="stylesheet" href="/static/custom.css">
  </head>
  <body>
    {{!base}}
    % if get('offline', True):
    <script src="/static/bootstrap-5.0.0-beta1/bootstrap.bundle.min.js"></script>
    % else:
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    % end
  </body>
</html>
