<?php include('server.php') ?>
<?php 
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php') ?>
<legend>Security settings</legend>
<p>Your account access token is <strong><?php echo $_SESSION['token']; ?></strong></p>
<form>
<table class="tui-table-grid"><tbody>
  <tr><td>Authentication options:</td></tr>
  <tr><td><label class="tui-checkbox">Token<input type="checkbox" checked/><span></span></label></td></tr>
  <tr><td><label class="tui-checkbox">Password (unavailable)<input type="checkbox" disabled/><span></span></label></td></tr>
</tbody></table>
</form>
</br>
In case your token got leaked, you can generate new token for your account:
<form action="security.php" method="post" style="text-align: center;"><button type="submit" class="tui-button" style="font-family:Perfect DOS VGA\ 437 Win; font-size:24px;" name="security">Regenerate Token</button></form>
<?php include('errors.php'); ?>
<script src="media/script.js"></script>
<?php include('footer.php') ?>
<?php endif;?>