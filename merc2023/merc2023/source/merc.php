<?php 
  include('server.php');
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php') ?>
<legend>Browser</legend>
<table class="tui-table-grid no-border" style="width: 100%;">
    <thead class="white-255-text tui-border-double orange-168-border" style="height:20%">
        <tr>
        <th style="width:20%"></th>
        <th>Alias</th>
        <th>Experience</th>
        <th>Weekly $ fee</th>
        <th>Specialty</th></tr>
    </thead>
    <tbody class="white-255-text tui-border-double orange-168-border">
        <tr>
        <?php 
        if (isset($_GET['alias'])){
            $alias = pg_escape_string($db_connect, $_GET['alias']);
        } 
        else { $alias = null; }

        $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM commandos WHERE alias = '$alias' LIMIT 1");
        if (pg_num_rows($results) == 1) 
        { 
            $commando = pg_fetch_all($results)[0];
            $theme = "Hiring ".$commando['alias']."";
            $token = $_SESSION['token'];
            echo '<td><img src="avatars/'.$commando['alias'].'.jpg" style="width:100%;height:100%;image-rendering:pixelated;"></td><td><p style="text-align:center;">'.$commando['alias'].'</p></td><td><p style="text-align:center;">'.$commando['xp'].'</p></td><td><p style="text-align:center;">'.$commando['price'].'</p></td>';
            $spec = explode('/', $commando['spec']);
            $counter = 0;
            echo '<td>';
            foreach ($spec as &$item) {echo '<p>'.$item.'</p>'; $counter++; if ($counter > 3) break;}
            echo '</td>';
            echo '<form method="post">
            <input name="alias" value="'.$commando['alias'].'" style="display: none"/>
            <input name="theme" value="'.$theme.'" style="display: none"/>';
            $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM messages WHERE theme = '$theme' AND sender_id = '$token' LIMIT 1");
        }?>
        </tr>
    </tbody>
</table><br>
Name your price: <input class="tui-input orange-168" name="payment" type="number" value="<?php echo $commando['price']?>"/><br><br>
Offer commentary: <input class="tui-input orange-168" name="commentary" type="text"/><br><br>
Location estimate: <select class="tui-input" name="location">
    <option value="SA">South America</option>
    <option value="A">Africa</option>
    <option value="ME">Middle East</option>
    <option value="EE">Eastern Europe</option>
    <option value="SEA">South-East Asia</option>
    <option value="NA">North America</option>
</select>
<?php
if ($commando['status'] && pg_num_rows($results) == 0) {
                echo '<button type="submit" name="request" class="tui-button" style="width: 200px">Make an offer</button></form>';
            } else {
                echo '<button type="submit" name="request" class="tui-button red-168 disabled" style="width: 200px" disabled>Unavailable</button></form>';
            } 
?>
<?php include('errors.php') ?>
<form method="get">
<p></p>
<button type="submit" formaction="browser.php" class="tui-button" style="width: 200px">Back</button>
</form>
<?php include('footer.php') ?>
<?php endif;?>