<?php
// Vérifier si le formulaire a été soumis
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (isset($_POST["pwd"]) && !empty($_POST["pwd"])) {
        $password = htmlspecialchars($_POST["pwd"]);
        echo "Le mot de passe saisi est : " . $password;
    } else {
        echo "Veuillez saisir un mot de passe.";
    }
}
?>
