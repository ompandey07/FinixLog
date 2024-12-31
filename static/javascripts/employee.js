feather.replace();

        document.getElementById('image-upload').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('image-preview');
                    preview.innerHTML = `<img src="${e.target.result}" alt="logo.png" class="w-full h-full object-cover">`;
                }
                reader.readAsDataURL(file);
            }
        });

        