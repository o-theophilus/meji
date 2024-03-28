<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let advert;
	console.log(advert);
	export let item;
	let input;
	let dragover = false;
	let error = {};
	let def_size = '300x300';
	let active_size = '300x300';
	let sizes = ['300x300', '300x600', '600x300', '900x300'];

	const remove_photo = async () => {
		error = {};

		$loading = 'removing . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${advert.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(active_size)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			active_size = def_size;
			$portal = {
				type: 'advert',
				data: resp.advert
			};
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

		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert_all/${advert.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			(active_size = def_size),
				($portal = {
					type: 'advert',
					data: resp.advert
				});
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
			} else if (!sizes.includes(dim)) {
				err = `${file.name} => invalid dimension`;
			} else if (advert[`photo_${dim}`]) {
				err = `${file.name} => already picked`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				files.push(file);
			}
		}

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
			if (!active_size.photo) {
				active_size = def_size;
			}
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: 'Advert Updated'
			};

			if (resp.error) {
				error.error = error.error ? `${error.error}, ${resp.error}` : resp.error;
			}
		} else {
			error = resp;
		}
	};
</script>

<img
	src={advert[`photo_${active_size}`] || '/image/item.png'}
	alt={item.name}
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
	{#each sizes as size}
		<img
			src={advert[`photo_${size}`] ? `${advert[`photo_${active_size}`]}/200` : '/image/item.png'}
			alt="{item.name} {size}"
			onerror="this.src='/image/item.png'"
			on:click={() => {
				error = {};
				active_size = size;
			}}
			class:active={active_size == size}
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
	>
		<!-- disabled={available_sizes.length >= 4} -->
		Add
	</Button>

	<Button class="hover_red" on:click={remove_photo} disabled={!advert[`photo_${active_size}`]}
		>Remove</Button
	>
</div>
<br />
<div class="row">
	<Button class="hover_red" on:click={delete_advert}>
		<!-- disabled={available_sizes.length <= 0} -->
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
