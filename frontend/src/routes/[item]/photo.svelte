<script>
	import { loading, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let item = {};
	let init_order = [...item.photos];

	let order_changed = false;
	let show_left_btn = true;
	let show_right_btn = true;

	let input;
	let files = [];
	let excess_files = [];
	let invalid_files = [];

	let active_photo = '';
	let dragover = false;
	let error = {};
	export let count = 10;
	export let edit_mode = false;

	const make_active = (photo, clear_error = true) => {
		if (clear_error) {
			error = {};
		}
		show_left_btn = true;
		show_right_btn = true;
		active_photo = photo || '/image/item.png';
		let i = item.photos.indexOf(active_photo);
		if (i == item.photos.length - 1) {
			show_right_btn = false;
		} else if (i == 0) {
			show_left_btn = false;
		}
	};

	const compare_order = () => {
		order_changed = false;
		for (let i in item.photos) {
			if (init_order[i] != item.photos[i]) {
				order_changed = true;
				break;
			}
		}
	};

	const order_right = () => {
		let index = item.photos.indexOf(active_photo);
		if (index < item.photos.length - 1) {
			item.photos.splice(index, 1);
			item.photos.splice(index + 1, 0, active_photo);

			item = item;
			make_active(active_photo);
			compare_order();
		}
	};

	const order_left = () => {
		let index = item.photos.indexOf(active_photo);
		if (index > 0) {
			item.photos.splice(index, 1);
			item.photos.splice(index - 1, 0, active_photo);

			item = item;
			make_active(active_photo);
			compare_order();
		}
	};

	const reorder_delete = async (method) => {
		error = {};

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/${item.key}`, {
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
			item = resp.item;

			$portal = item;
			init_order = [...item.photos];
			order_changed = false;

			if (method == 'delete') {
				make_active(item.photos[0]);
			}
		} else {
			error = resp;
		}
	};

	const on_input = () => {
		files = [];
		excess_files = [];
		invalid_files = [];
		error = {};

		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');
			if (media == 'image' && !['svg+xml', 'x-icon'].includes(type)) {
				if (files.length < count - item.photos.length) {
					files.push(file);
				} else {
					excess_files.push(file.name);
				}
			} else {
				invalid_files.push(file.name);
			}
		}

		files.length > 0 && upload_input();

		if (excess_files.length > 0) {
			error.error = `
			<strong>
				Excess File${excess_files.length > 1 ? 's' : ''}:
			</strong>
			<br/>
			${excess_files.join(', ')}`;
		}
		if (invalid_files.length > 0) {
			error.error = `${excess_files.length > 0 ? `${error.error}<br/><br/>` : ''}

			<strong>
				Invalid File${invalid_files.length > 1 ? 's' : ''}:
			</strong>
			<br/>
			${invalid_files.join(', ')}`;
		}
	};

	const upload_input = async () => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/${item.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			item = resp.item;

			$portal = item;
			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	$: make_active(item.photos[0]);
</script>

<button
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
	on:dragenter
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
>
	<img src={active_photo} alt={item.title} onerror="this.src='/image/item.png'" />
</button>
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
			<button
				on:click={() => {
					make_active(photo);
				}}
				class:active={active_photo == photo}
			>
				<img src="{photo}/200" alt={item.name} onerror="this.src='/image/item.png'" />
			</button>
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
		{#if item.photos.length < count}
			<Button
				name="Add ({count - item.photos.length})"
				class="primary tiny"
				on:click={() => {
					input.click();
				}}
			/>
		{/if}

		{#if item.photos.length > 0}
			<Button
				name="Remove"
				class="tiny"
				on:click={() => {
					reorder_delete('delete');
				}}
			/>
		{/if}

		{#if item.photos.length > 1}
			<Button
				disabled={!show_left_btn}
				name="<<"
				class="tiny"
				on:click={() => {
					order_left();
				}}
			/>
			<Button
				disabled={!show_right_btn}
				name=">>"
				class="tiny"
				on:click={() => {
					order_right();
				}}
			/>
			<Button
				disabled={!order_changed}
				name="Save Order"
				class="tiny"
				on:click={() => {
					reorder_delete('put');
				}}
			/>
		{/if}
	</div>
{/if}

<style>
	button {
		width: 100%;
		padding: 0;
		border: 2px solid transparent;
		border-radius: var(--sp1);

		overflow: hidden;
		/* background-color: transparent; */
	}
	button.edit_mode:hover,
	.dragover.edit_mode {
		border-color: var(--cl1);
		cursor: pointer;
	}

	img {
		width: 100%;
	}

	.row {
		display: flex;
		justify-content: center;
		gap: var(--sp1);
		flex-wrap: wrap;
	}

	.row button {
		--size: 50px;
		width: var(--size);
		height: var(--size);

		transition: var(--trans1);
	}

	.active,
	.row button:hover {
		border-color: var(--cl1);
		transform: scale(1.1);
		cursor: pointer;
	}
</style>
