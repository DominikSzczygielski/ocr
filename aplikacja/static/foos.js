        const image = document.getElementById("pdf-image");
        const canvas = document.getElementById("selection-canvas");
        const ctx = canvas.getContext("2d");
        const previewContainer = document.getElementById("preview-container");
        const previewImg = document.getElementById("preview-img");
        const copyBtn = document.getElementById("copy-btn");
        const sendBtn = document.getElementById("send-btn");
        const img_width = image.width;
        const img_height = image.height;
        const fixed_width = 900; //format proporcji A4
        const fixed_height= 1273; //format proporcji A4 900*1/sqrt(2)

        let startX, startY, endX, endY, isDragging = false;
        let croppedBlob = null;


        function resizeCanvas() {
            image.width = fixed_width;
            image.height = fixed_height;
            canvas.width = image.clientWidth;
            canvas.height = image.clientHeight;


        }
        window.onload = resizeCanvas;
        window.onresize = resizeCanvas;




/// następna strona
        document.getElementById("next").addEventListener("click", function() {
            currentUrl = window.location.href;
            window.location.href = "/aplikacja/pdf/3";
        });

/// poprzednia strona
        document.getElementById("prev").addEventListener("click", function() {
            currentUrl = window.location.href;
            window.location.href = "/aplikacja/pdf/2";
        });

        canvas.addEventListener("mousedown", (e) => {

            isDragging = true;
            startX = e.offsetX;
            startY = e.offsetY;

        });

        canvas.addEventListener("mousemove", (e) => {
            if (!isDragging) return;
            endX = e.offsetX;
            endY = e.offsetY;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.strokeRect(startX, startY, endX - startX, endY - startY);

        });

        canvas.addEventListener("mouseup", (e) => {
            isDragging = false;
            showPreview();
        });

 function ajax_send(obraz) {
            let formData = new FormData();

            formData.append("cropped_image", obraz, "selection.png");
            $.ajax({

                type: "POST",
                body: formData,
                headers: {
                "X-CSRFToken": CSRF_TOKEN
                },
                url: "/aplikacja/upload_selection/",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {

                document.getElementById("tekst").value=response.tekst;

                },
                error: function () {
                    alert("blad");
                }
                })};

        function getBlobFromCanvas(canvas) {
            return new Promise(resolve => {
                canvas.toBlob(blob => {
                    resolve(blob);
                }, "image/png");
            });
        }


        async function showPreview() { // funckja asynchroniczna
            const selectionWidth = endX - startX;
            const selectionHeight = endY - startY;

            if (selectionWidth <= 0 || selectionHeight <= 0) {
                previewContainer.style.display = "none";
                return;
            }

            const tempCanvas = document.createElement("canvas");
            const tempCtx = tempCanvas.getContext("2d");
            tempCanvas.width = selectionWidth;
            tempCanvas.height = selectionHeight;

            var x_shift = img_width / fixed_width
            var y_shift = img_height / fixed_height

            tempCtx.drawImage(
                image,
                startX*x_shift, startY*y_shift, selectionWidth*x_shift, selectionHeight*y_shift,
                0, 0, selectionWidth, selectionHeight
            );

            previewImg.src = tempCanvas.toDataURL("image/png");
            previewContainer.style.display = "block";

            croppedBlob = await getBlobFromCanvas(tempCanvas);
            ajax_send(croppedBlob);
        }


