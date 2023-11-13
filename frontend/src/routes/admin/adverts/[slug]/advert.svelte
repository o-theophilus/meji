<script>
	import { onMount } from 'svelte';
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let advert;
	let input;
	let dragover = false;
	let error = {};
	let def_size = '300x300';
	let active_photo = {
		size: def_size,
		photo: null
	};

	let available_sizes = [];
	const set_available_sizes = () => {
		available_sizes = [];
		for (const [dim, url] of Object.entries(advert.photos)) {
			if (url) {
				available_sizes.push(dim);
			}
		}
	};

	const remove_photo = async () => {
		error = {};

		$loading = 'removing . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert_photo/${advert.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(active_photo)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			advert = resp.advert;
			active_photo = {
				size: def_size,
				photo: advert.photos[def_size]
			};
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: available_sizes.length > 0 ? 'Photo deleted' : 'Advert Deleted'
			};
			set_available_sizes();
		} else {
			error = resp;
		}
	};

	const delete_advert = async () => {
		error = {};

		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${advert.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			advert = resp.advert;
			active_photo = {
				size: def_size,
				photo: advert.photos[def_size]
			};
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: 'Advert Deleted'
			};
			set_available_sizes();
		} else {
			error = resp;
		}
	};

	const get_dimension = (file) => {
		return new Promise((resolve, reject) => {
			var reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = function (e) {
				var image = new Image();
				image.src = e.target.result;
				image.onload = function () {
					resolve(`${this.width}x${this.height}`);
				};
			};
		});
	};

	const on_input = async () => {
		let files = [];
		error = {};

		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');
			let dim = await get_dimension(file);

			let err = '';
			if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
				err = `${file.name} => invalid file`;
			} else if (available_sizes.includes(dim)) {
				err = `${file.name} => already picked`;
			} else if (!['300x300', '300x600', '600x300', '900x300'].includes(dim)) {
				err = `${file.name} => invalid dimension`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				available_sizes.push(dim);
				files.push(file);
			}
		}

		set_available_sizes();
		files.length > 0 && upload_input(files);
	};

	const upload_input = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = `uploading photo${files.length > 1 ? 's' : ''} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${advert.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			advert = resp.advert;
			if (!active_photo.photo) {
				active_photo = {
					size: def_size,
					photo: advert.photos[def_size]
				};
			}
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: 'Advert Updated'
			};
			set_available_sizes();
			if (resp.error) {
				error.error = error.error ? `${error.error}, ${resp.error}` : resp.error;
			}
		} else {
			error = resp;
		}
	};

	onMount(async () => {
		active_photo = {
			size: def_size,
			photo: advert.photos[def_size]
		};
		set_available_sizes();
	});
</script>

<img
	src={active_photo.photo || '/image/item.png'}
	alt={advert.item.name}
	onerror="this.src='/image/item.png'"
	class:dragover
	on:click={() => {
		input.click();
	}}
	on:dragover|preventDefault={() => {
		dragover = true;
	}}
	on:dragleave|preventDefault={() => {
		dragover = false;
	}}
	on:drop={(e) => {
		dragover = false;
		e.preventDefault();
		input.files = e.dataTransfer.files;
		on_input();
	}}
	role="presentation"
/>
<input
	style:display="none"
	type="file"
	accept="image/*"
	multiple
	bind:this={input}
	on:change={(e) => {
		on_input();
	}}
/>

<br />
<br />

<div class="row">
	{#each Object.entries(advert.photos) as [size, photo]}
		<img
			src={photo ? `${photo}/200` : '/image/item.png'}
			alt="{advert.item.name} {size}"
			onerror="this.src='/image/item.png'"
			on:click={() => {
				error = {};
				active_photo = { size, photo };
			}}
			class:active={active_photo.size == size}
			role="presentation"
		/>
	{/each}
</div>

<br />
<div class="row">
	<Button
		class="primary"
		on:click={() => {
			input.click();
		}}
		disabled={available_sizes.length >= 4}
	>
		Add
	</Button>

	<Button class="hover_red" on:click={remove_photo} disabled={!active_photo.photo}
		>Remove</Button
	>
</div>
<br />
<div class="row">
	<Button class="hover_red" on:click={delete_advert} disabled={available_sizes.length <= 0}>
		Delete Advert
	</Button>
</div>

{#if error.error}
	<br />
	<span class="error">
		{error.error}
	</span>
	<br />
{/if}

<style>
	img {
		border: 2px solid transparent;
		border-radius: var(--sp1);
		width: 100%;
		transition: var(--trans1);
	}

	img:hover,
	img.dragover {
		border-color: var(--cl1);
		cursor: pointer;
	}

	.row {
		display: flex;
		justify-content: center;
		gap: var(--sp1);
		flex-wrap: wrap;
	}

	.row img {
		--size: 50px;
		width: var(--size);
		height: var(--size);
	}

	.active {
		border-color: var(--cl1);
		transform: scale(1.1);
	}
</style>
