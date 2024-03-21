<script>
	import { loading, portal, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let item = {};
	export let edit_mode = false;

	let input;
	let active_photo = item.photos[0] || '';
	let init_order = [...item.photos];
	let dragover = false;
	let count = 10;
	let error = {};

	const move_right = (dir = true) => {
		error = {};

		let i = item.photos.indexOf(active_photo);
		item.photos.splice(i, 1);
		i = dir ? i + 1 : i - 1;
		item.photos.splice(i, 0, active_photo);
		item = item;
	};

	const reorder_delete = async (method) => {
		error = {};

		$loading = `${method == 'delete' ? 'deleting' : 'saving'} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/photo/${item.key}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				photos: item.photos,
				active_photo
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			init_order = [...resp.item.photos];

			let msg = 'Order saved';
			if (method == 'delete') {
				msg = 'Photo deleted';
				active_photo = item.photos[0] || '';
			}

			$portal = {
				type: 'item',
				data: resp.item
			};
			$toast = {
				status: 200,
				message: msg
			};
		} else {
			error = resp;
		}
	};

	const on_input = () => {
		error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');

			let err = '';
			if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
				err = `${file.name} => invalid file`;
			} else if (files.length + item.photos.length >= count) {
				err = `${file.name} => excess file`;
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

		$loading = 'uploading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/photo/${item.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			// item = resp.item;
			init_order = [...resp.item.photos];
			active_photo = active_photo || item.photos[0];
			$portal = {
				type: 'item',
				data: resp.item
			};
			$toast = {
				status: 200,
				message: 'Photo added'
			};

			if (resp.error) {
				error.error = error.error ? `${error.error}, ${resp.error}` : resp.error;
			}
		} else {
			error = resp;
		}
	};

	$: if (!item.photos.includes(active_photo)) {
		active_photo = item.photos[0] || '';
	}
</script>

<img
	src={active_photo || '/image/item.png'}
	alt={item.title}
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
		{#each item.photos as photo}
			<img
				src="{photo}/200"
				alt={item.name}
				onerror="this.src='/image/item.png'"
				on:click={() => {
					error = {};
					active_photo = photo;
				}}
				class:active={active_photo == photo}
				role="presentation"
			/>
		{/each}
	</div>
{/if}

{#if edit_mode}
	<br />
	<div class="row">
		<Button
			class="primary"
			on:click={() => {
				input.click();
			}}
			disabled={item.photos.length >= count}
		>
			Add ({count - item.photos.length})
		</Button>

		<Button
			class="hover_red"
			on:click={() => {
				reorder_delete('delete');
			}}
			disabled={item.photos.length == 0}
		>
			Remove
		</Button>
		<Button
			disabled={item.photos.length <= 1 || item.photos[0] == active_photo}
			on:click={() => {
				move_right(false);
			}}
		>
			&lt;
		</Button>
		<Button
			disabled={item.photos.length <= 1 || item.photos[item.photos.length - 1] == active_photo}
			on:click={() => {
				move_right();
			}}
		>
			&gt;
		</Button>
		<Button
			disabled={JSON.stringify(init_order) == JSON.stringify(item.photos)}
			on:click={() => {
				reorder_delete('put');
			}}
		>
			Save Order
		</Button>
	</div>

	{#if error.error}
		<br />
		<span class="error">
			{error.error}
		</span>
		<br />
	{/if}
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
