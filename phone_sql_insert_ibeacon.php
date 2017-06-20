<?php

        $device_uuid = $key_values[0];
        $timestamp = $key_values[1];
        $beaconNID = $key_values[2];

        $cad = "INSERT INTO phone_beacon (device_uuid,timestamp,beaconNID) VALUES('"
                                .$device_uuid."','".$timestamp."','".$beaconNID."')";

        $q = mysqli_query($conn,$cad);

        if($q)
                echo "insert beacon information to sql success";
        else
                echo "Insert fail";
?>
