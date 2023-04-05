<?php 
  include('server.php');
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php')?>
<div class="tui-tabs">
    <ul>
		<?if (isset($_GET['incoming'])):?>
        <li><a class="tui-tab active" data-tab-content="tab-1-content">Incoming</a></li>
        <li><a class="tui-tab" data-tab-content="tab-2-content">Outgoing</a></li>
        <li><a class="tui-tab" data-tab-content="tab-3-content">New Message</a></li>
		<?elseif (isset($_GET['outgoing'])):?>
		<li><a class="tui-tab" data-tab-content="tab-1-content">Incoming</a></li>
        <li><a class="tui-tab active" data-tab-content="tab-2-content">Outgoing</a></li>
        <li><a class="tui-tab" data-tab-content="tab-3-content">New Message</a></li>
		<?else:?>
		<li><a class="tui-tab active" data-tab-content="tab-1-content">Incoming</a></li>
        <li><a class="tui-tab" data-tab-content="tab-2-content">Outgoing</a></li>
        <li><a class="tui-tab" data-tab-content="tab-3-content">New Message</a></li>
		<?endif;?>
    </ul>
</div>
<div id="tab-1-content" class="tui-tab-content">
<br>
<?php 
	if(isset($_SESSION['token'])) {$receiver_id = $_SESSION['token']; }
	else { $receiver_id = ''; }
	$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM messages WHERE receiver_id='$receiver_id'");
	if (pg_num_rows($results) != 0) {
		$messages = pg_fetch_all($results);
		if (isset($_GET['page']) && is_numeric($_GET['page']) && $_GET['page'] > 0){
			$offset = $_GET['page'] - 1;
		} else {
			$offset = 0;
		}
		for ($i = (count($messages) - $offset*5) - 1; $i >= (count($messages) - $offset*5 - 5) && $i >= 0; $i--) :?>
			<?php 
			$token2 = $messages[$i]['sender_id'];
			$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT first_name, last_name FROM profiles WHERE token='$token2' LIMIT 1");
			if (pg_num_rows($results) != 0) $receiver = pg_fetch_all($results)[0];
			?>
			<div class="tui-panel black-255-text full-width">
			    <div class="tui-panel-header">
					<span class="red-168-text left"><?echo $messages[$i]['timemark']?></span>
					Theme: <?echo $messages[$i]['theme']?> from <?echo $receiver['first_name']?> <?echo $receiver['last_name']?>
			    </div>
			    <div class="tui-panel-content white-255-text" style="text-overflow: ellipsis;overflow: hidden; width:640px">
			        <?echo $messages[$i]['message']?>
			    </div>
			</div>
		<?endfor;
	} else { echo 'No messages!'; }
?>
<?php if(isset($offset)):?>
<form method="get">
<div class="tui-window orange-168" style="position:absolute; width: 668px; left: 18px; bottom:15px">
    <fieldset class="tui-fieldset tui-border-solid center">
	<input name="incoming" hidden/>
<?php if ($offset > 0 && (($offset + 1)*5) <= count($messages)):?>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php elseif ((($offset + 1)*5) > count($messages) && $offset != 0):?>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php elseif (count($messages) <= 5):?>
    <button type="submit" formaction="messenger.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php else:?>
    <button type="submit" formaction="messenger.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php endif;?>
</fieldset>
</div>
</form>
<?php endif;?>
</div>
<div id="tab-2-content" class="tui-tab-content">
<br>
<?php 
	if(isset($_SESSION['token'])) {$receiver_id = $_SESSION['token']; }
	else { $receiver_id = ''; }
	if ($_SESSION['status'] == '1'){$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM messages");} else {
	$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT * FROM messages WHERE sender_id='$receiver_id'"); }
	if (pg_num_rows($results) != 0) {
		$messages = pg_fetch_all($results);
		if (isset($_GET['page']) && is_numeric($_GET['page']) && $_GET['page'] > 0){
			$offset = $_GET['page'] - 1;
		} else {
			$offset = 0;
		}
		for ($i = (count($messages) - $offset*5) - 1; $i >= (count($messages) - $offset*5 - 5) && $i >= 0; $i--) :?>
			<?php 
			$token2 = $messages[$i]['receiver_id'];
			$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT first_name, last_name FROM profiles WHERE token='$token2' LIMIT 1");
			if (pg_num_rows($results) != 0) $receiver = pg_fetch_all($results)[0];
			?>
			<div class="tui-panel black-255-text full-width">
			    <div class="tui-panel-header">
				<span class="red-168-text left"><?echo $messages[$i]['timemark']?></span>
					Theme: <?echo $messages[$i]['theme']?> to <?echo $receiver['first_name']?> <?echo $receiver['last_name']?>
			    </div>
			    <div class="tui-panel-content white-255-text" style="text-overflow: ellipsis;overflow: hidden; width:640px">
			        <?echo $messages[$i]['message']?>
			    </div>
			</div>
		<?endfor;
	} else { echo 'No messages!'; }
?>
<?php if(isset($offset)):?>
<form method="get">
<div class="tui-window orange-168" style="position:absolute; width: 668px; left: 18px; bottom:15px">
    <fieldset class="tui-fieldset tui-border-solid center">
	<input name="outgoing" hidden/>
<?php if ($offset > 0 && (($offset + 1)*5) <= count($messages)):?>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php elseif ((($offset + 1)*5) > count($messages) && $offset != 0):?>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php elseif (count($messages) <= 5):?>
    <button type="submit" formaction="messenger.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php else:?>
    <button type="submit" formaction="messenger.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
	<span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($messages)/5)?></span>
    <button type="submit" formaction="messenger.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php endif;?>
</fieldset>
</div>
</form>
<?php endif;?>
</div>
<div id="tab-3-content" class="tui-tab-content">
<br>
<form method="post">
<div class="tui-panel black-255-text full-width">
    <div class="tui-panel-header">
		Theme:<input class="tui-input white-255 black-255-text" name="theme" type="text"/>
		To: <select class="tui-input white-255 black-255-text" name="receiver">
		<?php 
		$results = pg_query(pg_connect($_SESSION['db_string']),"SELECT first_name, last_name, dob FROM profiles");
		if (pg_num_rows($results) != 0) { 
			$receivers = pg_fetch_all($results);
			foreach ($receivers as &$item):
			?>
		    	<option value="<?php echo $item['first_name'] . ":" . $item['last_name'] . ":" . $item['dob']?>"><?php echo $item['first_name'] . " " . $item['last_name']?></option>
			<?php endforeach; }?>
		</select>
    </div>
    <div class="tui-panel-content white-255-text" style="text-overflow: ellipsis;overflow: hidden; width:640px">
		Contents:<input class="tui-input blue-168" name="contents" type="text"/>
    </div>
</div>
<p style="text-align:center;"><button type="submit" name="message" class="tui-button" style="width: 200px">Send</button></p>
</form>
</div>
<?php include('footer.php')?>
<?php endif;?>