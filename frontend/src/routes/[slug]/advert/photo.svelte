<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import { onMount } from 'svelte';

	export let item;
	export let advert;
	export let edit_mode = false;
	let input;
	let active_photo = {};
	let dragover = false;
	let error = {};
	let available_sizes = [];

	const make_active = (dict_) => {
		active_photo = dict_;

		available_sizes = [];
		for (const [dim, url] of Object.entries(advert.photos)) {
			if (url) {
				available_sizes.push(dim);
			}
		}
	};

	const delete_photo = async () => {
		error = {};

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert_photo/${item.key}`, {
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
			$portal = resp.advert;
			make_active(active_photo);

			$toast = {
				status: 200,
				message: available_sizes.length > 0 ? 'Photo deleted' : 'Advert Deleted'
			};
		} else {
			error = resp;
		}
	};

	const delete_advert = async () => {
		error = {};

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${item.key}`, {
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
			$portal = resp.advert;

			let size = '300x300';
			make_active({ size, photo: advert.photos[size] });

			$toast = {
				status: 200,
				message: 'Advert Deleted'
			};
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

		make_active(active_photo);
		files.length > 0 && upload_input(files);
	};

	const upload_input = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${item.key}`, {
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
			$portal = resp.advert;
			make_active(active_photo);

			$toast = {
				status: 200,
				message: 'Advert Updated'
			};
			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	onMount(() => {
		let size = '300x300';
		make_active({ size, photo: advert.photos[size] });
	});
</script>

<img
	src={active_photo.photo || '/image/item.png'}
	alt={item.name}
	onerror="this.src='/image/item.png'"
	class:dragover
	class:edit_mode
	on:click={() => {
		if (edit_mode) {
			input.click();
		}
	}}
	on:dragover|preventDefault={() => {
		dragover = true;
	}}
	on:dragleave|preventDefault={() => {
		dragover = false;
	}}
	on:drop={(e) => {
		dragover = false;
		if (edit_mode) {
			e.preventDefault();
			input.files = e.dataTransfer.files;
			on_input();
		}
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

{#if item.photos.length > 1}
	<div class="row">
		{#each Object.entries(advert.photos) as [size, photo]}
			<img
				src={photo ? `${photo}/200` : '/image/item.png'}
				alt="{item.name} {size}"
				onerror="this.src='/image/item.png'"
				on:click={() => {
					error = {};
					make_active({ size, photo });
				}}
				class:active={active_photo.size == size}
				role="presentation"
			/>
		{/each}
	</div>
{/if}

{#if edit_mode}
	{#if error.error}
		<br />
		<span class="error">
			{@html error.error}
		</span>
		<br />
	{/if}

	<br />
	<div class="row">
		<Button
			class="primary small"
			on:click={() => {
				input.click();
			}}
			disabled={available_sizes.length >= 4}
		>
			Add
		</Button>

		<Button class="small" on:click={delete_photo} disabled={!active_photo.photo}>Remove</Button>
	</div>
	<Button class="small" on:click={delete_advert} disabled={available_sizes.length <= 0}>
		Delete Advert
	</Button>
{/if}

<style>
	img {
		border: 2px solid transparent;
		border-radius: var(--sp1);
		width: 100%;
		transition: var(--trans1);
	}

	.row img:hover,
	.edit_mode:hover,
	.edit_mode.dragover {
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
