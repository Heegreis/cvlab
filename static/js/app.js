function process() {
	imagebox = $('#output_img')
	input = $('#imageinput')[0]
	if (input.files && input.files[0]) {
		let formData = new FormData();
		formData.append('image', input.files[0]);
		formData.append('algorithm', 'gosh');
		$.ajax({
			url: "/process", // fix this to your liking
			type: "POST",
			data: formData,
			cache: false,
			processData: false,
			contentType: false,
			error: function (data) {
				console.log("upload error", data);
				console.log(data.getAllResponseHeaders());
			},
			success: function (data) {
				// alert("hello"); // if it's failing on actual server check your server FIREWALL + SET UP CORS
				bytestring = data['status']
				image = bytestring.split('\'')[1]
				imagebox.attr('src', 'data:image/jpeg;base64,' + image)
			}
		});
	}
};


function readUrl(input) {
	imagebox = $('#input_img')
	console.log("evoked readUrl")
	if (input.files && input.files[0]) {
		let reader = new FileReader();
		reader.onload = function (e) {
			// console.log(e)
			imagebox.attr('src', e.target.result);
			// imagebox.height(300);
			// imagebox.width(300);
		}
		reader.readAsDataURL(input.files[0]);
	}
}

// this is the id of the form
$("#idForm").submit(function(e) {

    var form = $(this);
	var url = form.attr('action');

    $.ajax({
			type: "POST",
			url: url,
			data: form.serialize(), // serializes the form's elements.
			// cache: false,
			success: function()
			{
			//    alert(data); // show response from the php script.
			console.log('sucess!')
			},
			error: function (data) {
				console.log("upload error", data);
				console.log(data.getAllResponseHeaders());
			}
    });

	e.preventDefault(); // avoid to execute the actual submit of the form.
});