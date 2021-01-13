% rebase('base.tpl', title=title)
<nav class="navbar navbar-expand-lg bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">천국의 문 v2.10.6</a>
    <span class="navbar-text w-300">
      {{name}} ({{username}}@) 
      % if is_admin:
      <i class="bi-shield-fill-check"></i>
      % else:
      <i class="bi-shield-slash-fill"></i>
      % end
       /
      <a href="/logout"><i class="bi-box-arrow-right"></i> (로그 아웃)</a>
    </span>
  </div>
</nav>
<div class="container" style="padding-top: 20px">
    {{!base}}
</div>
