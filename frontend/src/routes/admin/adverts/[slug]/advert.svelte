<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let advert;
	export let item;
	export let sizes;
	export let photo_length;
	let input;
	let dragover = false;
	let error = {};
	let active_size = sizes[0];

	const remove_photo = async () => {
		error = {};

		$loading = 'removing . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/photo/${advert.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ size: active_size })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			active_size = sizes[0];
			$portal = {
				type: 'advert',
				data: resp.advert
			};
			$toast = {
				status: 200,
				message: photo_length(resp.advert) > 0 ? 'Photo deleted' : 'Advert Deleted'
			};
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
			(active_size = sizes[0]),
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

		let new_pick = [];

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
				err = `${file.name} => slot occupied`;
			} else if (new_pick.includes(dim)) {
				err = `${file.name} => slot picked`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				new_pick.push(dim);
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
				active_size = sizes[0];
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
	class:can_hover={photo_length(advert) < sizes.length}
	on:click={() => {
		if (photo_length(advert) < sizes.length) {
			input.click();
		}
	}}
	on:dragover|preventDefault={() => {
		dragover = photo_length(advert) < sizes.length;
	}}
	on:dragleave|preventDefault={() => {
		dragover = false;
	}}
	on:drop={(e) => {
		dragover = false;
		if (photo_length(advert) < sizes.length) {
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

<div class="row">
	{#each sizes as x}
		<img
			src={advert[`photo_${x}`] ? `${advert[`photo_${x}`]}/200` : '/image/item.png'}
			alt="{item.name} {x}"
			onerror="this.src='/image/item.png'"
			on:click={() => {
				error = {};
				active_size = x;
			}}
			class:active={active_size == x}
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
		disabled={sizes.length == photo_length(advert)}
	>
		Add
	</Button>

	<Button class="hover_red" on:click={remove_photo} disabled={!advert[`photo_${active_size}`]}
		>Remove</Button
	>
</div>
<br />
<div class="row">
	<Button class="hover_red" on:click={delete_advert} disabled={photo_length(advert) == 0}>
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

	.row img:hover,
	img:hover.can_hover,
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
