% rebase('inside-base.tpl', title='C&C v.2.10.6', username=username, name=name, is_admin=is_admin)

<h1>Control Server</h1>
<h2>Normal Operations:</h2>
<ul>
  <li><a href="/stats">View stats</a></li>
  <li><a href="/upload">Upload a key</a></li>
</ul>
% if is_admin:
<h2>Admin Operations</h2>
<ul>
  <li><a href="/view_logs">View logs (Admin only)</a></li>
</ul>
% else:
<h2>Admin Operations - Disabled</h2>
<ul>
  <li><a href="/enable_admin">Enable administrator mode</a></li>
  <li><a href="/view_logs">View logs (Disabled, admin only)</a></li>
</ul>
% end
