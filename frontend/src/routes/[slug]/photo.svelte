<script>
	import { loading, portal, toast, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Advert from './_advert.svelte';

	export let item = {};
	export let edit_mode = false;

	let order_changed = false;
	let show_left_btn = true;
	let show_right_btn = true;

	let input;
	let excess_files = [];
	let invalid_files = [];

	let active_photo;
	let init_order = [...item.photos];
	let dragover = false;
	let count = 10;
	let error = {};

	const make_active = (photo) => {
		error = {};

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

	const order = (dir = 'right') => {
		let index = item.photos.indexOf(active_photo);
		item.photos.splice(index, 1);

		if (dir == 'right' && index < item.photos.length) {
			item.photos.splice(index + 1, 0, active_photo);
		} else if (dir == 'left' && index > 0) {
			item.photos.splice(index - 1, 0, active_photo);
		}

		item = item;
		make_active(active_photo);

		order_changed = false;
		for (let i in item.photos) {
			if (init_order[i] != item.photos[i]) {
				order_changed = true;
				break;
			}
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
			init_order = [...item.photos];
			order_changed = false;

			let msg = 'Order saved';
			if (method == 'delete') {
				$portal = {
					type: 'item',
					data: resp.item
				};
				make_active(item.photos[0]);
				msg = 'Photo deleted';
			}

			$toast = {
				status: 200,
				message: msg
			};
		} else {
			error = resp;
		}
	};

	const on_input = () => {
		let files = [];
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

		files.length > 0 && upload_input(files);

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

	const upload_input = async (files) => {
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
			init_order = [...item.photos];
			$portal = {
				type: 'item',
				data: resp.item
			};
			make_active(item.photos[0]);

			$toast = {
				status: 200,
				message: 'Photo added'
			};

			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	$: if (!item.photos.includes(active_photo)) {
		make_active(item.photos[0]);
	}

	let advert = {};
	$: if ($portal && $portal.type == 'advert') {
		advert = $portal.data;
		$portal = '';
	}
</script>

<img
	src={active_photo}
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
					make_active(photo);
				}}
				class:active={active_photo == photo}
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
			disabled={item.photos.length >= count}
		>
			Add ({count - item.photos.length})
		</Button>

		<Button
			class="small hover_red"
			on:click={() => {
				reorder_delete('delete');
			}}
			disabled={item.photos.length == 0}
		>
			Remove
		</Button>
		<Button
			disabled={!show_left_btn}
			class="small"
			on:click={() => {
				order('left');
			}}
		>
			<SVG type="arrow_left" size="16" />
		</Button>
		<Button
			disabled={!show_right_btn}
			class="small"
			on:click={() => {
				order('right');
			}}
		>
			<SVG type="arrow_right" size="16" />
		</Button>
		<Button
			disabled={!order_changed}
			class="small"
			on:click={() => {
				reorder_delete('put');
			}}
		>
			Save Order
		</Button>
	</div>
	<br />
	<div class="row">
		<Button
			class="small"
			on:click={() => {
				$module = {
					module: Advert,
					item,
					advert
				};
			}}
		>
			Advert
		</Button>
	</div>
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
