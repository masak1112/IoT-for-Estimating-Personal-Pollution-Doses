<?php
        $f = fopen('/tmp/eco.sql','a');
        $db_name = "db_name";
        $mysql_username = "mysql_username";
        $mysql_password = "password";
        $server_name = "server_name";
        $conn = mysqli_connect($server_name, $mysql_username, $mysql_password,$db_name);

        $conn->set_character('utf8');
        if($conn) {
                echo "connection success";
                }else {
                echo "connection fail";
                        }

        
        $keys=array_keys($_POST);
        $key_values=array_values($_POST);
        fprintf($f,"POST : %s \n KEY: %s \n key_values %s \n email:%s \n",print_r($_POST,TRUE),
        print_r($keys,TRUE),print_r($key_values,TRUE),print_r($key_values[5],TRUE));

        $email=$key_values[0];
        $bd = $key_values[1];
        $sex = $key_values[2];
        $respiratory = $key_values[3];
        $cardiovascular = $key_values[4];
        $pulmonary = $key_values[5];

        fprintf($f,"%s \n","and here as well");


        fprintf($f,"%s : %s : %s : %d : %d : %d \n",$email,
                        $bd,$sex,$respiratory,$cardiovascular,
                        $pulmonary);

        $cad = "INSERT INTO individual_information (email,birthday,".
                                "sex,respiratory".
                                ",cardiovascular,pulmonary) VALUES('"
                                .$email."','".$bd."','".$sex."','".$respiratory.
                                "','".$cardiovascular."','".$pulmonary."')";
        echo $cad."\n";
        fprintf($f,"%s\n",$cad);
        fclose($f);
        $q= mysqli_query($conn,$cad);
        if($q) {
                echo "insert success";
                }else {
                echo "insert fails";
                }
?>

