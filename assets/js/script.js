
// script.js minimal pour site statique - Version corrigée
document.addEventListener('DOMContentLoaded', function() {
    console.log('Site chargé avec succès !');
    
    // Exemple d'interaction simple qui n'interfère pas avec les animations
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function() {
            // Au lieu de alert() qui bloque le thread, on utilise une animation CSS
            this.classList.add('clicked');
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 300);
            
            // Changement de texte sans bloquer l'UI
            const message = document.getElementById('message');
            if (message) {
                message.textContent = 'Bouton cliqué !';
                setTimeout(() => {
                    message.textContent = 'Bienvenue sur mon site !';
                }, 2000);
            }
        });
    }
    
    // Exemple de modification non-bloquante
    const title = document.querySelector('h1');
    if (title) {
        // Utilise une classe CSS au lieu de modifier le style directement
        title.classList.add('styled-title');
    }
    
    // Animation simple en JavaScript (non-bloquante)
    let counter = 0;
    const animateElement = document.getElementById('animate-me');
    if (animateElement) {
        function smoothAnimation() {
            counter += 0.05;
            animateElement.style.transform = `translateX(${Math.sin(counter) * 20}px)`;
            requestAnimationFrame(smoothAnimation);
        }
        smoothAnimation();
    }
});