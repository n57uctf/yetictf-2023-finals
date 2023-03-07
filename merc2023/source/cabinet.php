<?php 
  include('server.php');
  if (!isset($_SESSION['token'])) : header('Location: ../index.php');
  else :
?>
<?php include('header.php') ?>
<legend>Cabinet</legend>
<?php if ($_SESSION['status'] == "Merchant"){
  $token_type = "contractor_token";
} else { $token_type = "executor_token"; }
$token = $_SESSION['token'];
?>
<table class="tui-table no-border hovered-white" style="width: 100%;">
    <thead class="white-255-text orange-168-border" style="height:50px">
        <tr>
        <?php
        if ($token_type == 'executor_token'){echo '<th></th>';}
        else  { echo '<th>Alias</th>';}
        ?>
        <th style="width:50%">Commentary</th>
        <th style="width:15%">Offer</th>
        <th></tr>
    </thead>
    <tbody class="white-255-text orange-168-border">
        <?php 
          $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM contracts WHERE ".$token_type." = '$token'");
          if (pg_num_rows($results) != 0) {
            $contracts = pg_fetch_all($results);
            $aliases = [];
            foreach ($contracts as &$item) {
              $commando_token = $item['executor_token'];
              $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT description FROM profiles WHERE token = '$commando_token'");
              if (pg_num_rows($results) != 0) {
                $descriptions = pg_fetch_all($results);
                $aliases += [$commando_token => $descriptions[0]['description']];
              }
            }
            if (isset($_GET['page']) && is_numeric($_GET['page']) && $_GET['page'] > 0){
                $offset = $_GET['page'] - 1;
            } else {
                $offset = 0;
            }
            for ($i = $offset*3; $i < $offset*3 + 3 && $i < count($contracts); $i++) :?><?php 
              echo '<tr style="height:100px">';
              if ($token_type == 'executor_token') {echo '<td></td>';} 
              else { echo '<td><p style="text-align:center;">'.$aliases[$contracts[$i]['executor_token']].'</p></td>';}
              echo '<td><p style="text-overflow: ellipsis;overflow-wrap: anywhere; width: 300px">'.$contracts[$i]['commentary'].'</p></td>';
            echo '<td><p style="text-align:center;">'.$contracts[$i]['payment'].'</p></td>';
            if ($contracts[$i]['executor_token'] == $_SESSION['token'] && $contracts[$i]['status'] == 'pending'){ echo '<td><form method="get"><input name="cid" value="'.$contracts[$i]['id'].'" style="display: none"/><p style="text-align:center;"><button type="submit" name="status" value="accept" class="tui-button">Accept</button><button type="submit" name="status" value="decline" class="tui-button red-168">Decline</button></p></form></td>'; }
            else { echo '<td><p style="text-align:center;">'.$contracts[$i]['status'].'</p></td>'; }
            echo '</tr>';
            endfor;
          } else {echo '<tr><td><p style="text-align:center;">No</p></td><td><p style="text-align:center;">contracts</p></td><td><p style="text-align:center;">available</p></td></tr>';}?>
    </tbody>
</table>
<?php if(isset($offset)):?>
<form method="get">
<div class="tui-window orange-168" style="position:absolute; width: 668px; left: 18px; bottom:15px">
    <fieldset class="tui-fieldset tui-border-solid center">
<?php if ($offset > 0 && (($offset + 1)*3) >= count($contracts)):?>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($contracts)/3)?></span>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php elseif ((($offset + 1)*3) <= count($contracts) && $offset != 0):?>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset?>" class="tui-button left" style="width: 200px">Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($contracts)/3)?></span>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php elseif (count($contracts) <= 3):?>
    <button type="submit" formaction="cabinet.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($contracts)/3)?></span>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset+2?>" class="tui-button red-168 disabled right" style="width: 200px" disabled>Next</button>
<?php else:?>
    <button type="submit" formaction="cabinet.php?" name="page" value="<?echo $offset?>" class="tui-button red-168 disabled left" style="width: 200px" disabled>Previous</button>
    <span class="center">Page <?php echo $offset + 1?>/<?php echo ceil(count($contracts)/3)?></span>
    <button type="submit" formaction="cabinet.php" name="page" value="<?echo $offset+2?>" class="tui-button right" style="width: 200px">Next</button>
<?php endif;?>
</fieldset>
</div>
</form>
<?php endif;?>
<script src="media/script.js"></script>
<?php include('footer.php') ?>
<?php endif;?>