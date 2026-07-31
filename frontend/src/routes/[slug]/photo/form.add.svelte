<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let { ops } = $props();
	let input;
	let dragover = $state(false);

	const on_input = () => {
		ops.error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];

			let err = '';
			if (!['image/jpeg', 'image/png'].includes(file.type)) {
				err = `${file.name} => invalid file`;
			}

			if (err) {
				ops.error.error = ops.error.error ? `${ops.error.error} <br/> ${err}` : err;
			} else {
				files.push(file);
			}
		}

		files.length > 0 && upload(files);
		input.value = '';
	};

	const upload = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		loading.open('uploading . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/${ops.key}/file`, {
			method: 'post',
			headers: {
				Authorization: app.token
			},
			body: formData
		});
		let result = await response.json();
		loading.close();
		input.value = '';

		if (response.status == 200) {
			if (ops.files.length == 0) {
				ops.active = result.item.files[0];
			}
			ops.files = result.item.files;
			module.value.update(result.item);
			notify.open('Photo added');

			if (result.error) ops.error = result;
		} else {
			ops.error = result;
		}
	};

	let dim = $state([1, 1]);
</script>

<img
	src={ops.active}
	alt={ops.name}
	class="main"
	class:dragover
	style:--ar={dim[0] / dim[1]}
	onclick={() => {
		input.click();
	}}
	ondragover={(e) => {
		e.preventDefault();
		dragover = true;
	}}
	ondragleave={(e) => {
		e.preventDefault();
		dragover = false;
	}}
	ondrop={(e) => {
		dragover = false;

		e.preventDefault();
		input.files = e.dataTransfer.files;
		on_input();
	}}
	onerror={(e) => (e.target.src = '/no_photo.png')}
	role="presentation"
/>
<input
	style:display="none"
	type="file"
	accept="image/jpeg, image/png"
	multiple
	bind:this={input}
	onchange={on_input}
/>

<style>
	img {
		width: 100%;
		aspect-ratio: var(--ar);
		border-radius: 8px;
		outline: 2px solid transparent;
		object-fit: cover;
		cursor: pointer;
		background-color: var(--bg1);

		transition: outline-color 0.2s ease-in-out;
	}

	.dragover,
	img:hover {
		outline-color: var(--cl1);
	}
</style>
