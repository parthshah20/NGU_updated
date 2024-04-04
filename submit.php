<?php
$name = $_POST['name'];
$equations = $_POST['equations'];
$const = $_POST['const'];

// $data = "Name: $name\nEmail: $email\nMessage: $message\n";
$data1 = "$equations";
$data2 = "$const";

$file1 = "eq_$name.txt";
$file2 = "const_$name.txt";

// Open the file to append
$current = file_get_contents($file1);
$current .= $data1;

// Write the contents back to the file
file_put_contents($file1, $current);


// Open the file to append
$current = file_get_contents($file2);
$current .= $data2;

// Write the contents back to the file
file_put_contents($file2, $current);

echo "Form submitted successfully!";
?>