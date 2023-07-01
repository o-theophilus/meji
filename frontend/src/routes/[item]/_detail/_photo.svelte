<script>
	import { module, tick } from '$lib/store.js';

	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';
	import HR from '$lib/comp/hr.svelte';

	import Add from './_photo_add.svelte';

	export let data;
	let { item } = data;
	item.active_photo = item.photos.length > 0 ? item.photos[0] : '/image/item.png';

	let init_order = [...item.photos];
	let order_changed = false;

	let error = '';

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
		let index = item.photos.indexOf(item.active_photo);
		if (index < item.photos.length - 1) {
			item.photos.splice(index, 1);
			item.photos.splice(index + 1, 0, item.active_photo);

			item = item;
			compare_order();
		}
	};

	const order_left = () => {
		let index = item.photos.indexOf(item.active_photo);
		if (index > 0) {
			item.photos.splice(index, 1);
			item.photos.splice(index - 1, 0, item.active_photo);

			item = item;
			compare_order();
		}
	};

	const submit = async (method) => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}photo_item/${item.key}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				let _temp = item.active_photo;
				item = resp.data.item;
				tick(item);

				item.active_photo = _temp;
				if (method == 'delete') {
					item.active_photo = '/image/item.png';
					if (item.photos.length > 0) {
						item.active_photo = item.photos[0];
					}
				}

				init_order = [...item.photos];
				order_changed = false;
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Manage Photo</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		<p>Add, Remove, Reorder Photos</p>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<img src={item.active_photo} alt={item.name} />
		{#if item.photos.length > 1}
			<div class="slide">
				{#each item.photos as photo}
					<img
						src={photo}
						alt={item.name}
						class:active={item.active_photo == photo}
						on:click={() => {
							item.active_photo = photo;
						}}
					/>
				{/each}
			</div>

			<HR />

			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}

			<div class="inputGroup horizontal">
				<Button name="Left" on:click={order_left} />
				<Button name="Right" on:click={order_right} />
				{#if order_changed}
					<Button
						name="Accept"
						on:click={() => {
							submit('put');
						}}
					/>
				{/if}
			</div>
		{/if}

		<HR />

		<div class="inputGroup horizontal">
			{#if item.photos.length < 10}
				<Button
					name="Add"
					class="primary"
					on:click={() => {
						$module = {
							module: Add,
							data: {
								item
							}
						};
					}}
				/>
			{/if}

			{#if item.photos.length > 0}
				<Button
					name="Remove"
					on:click={() => {
						submit('delete');
					}}
				/>
			{/if}
		</div>
	</form>
</Form>

<style>
	img {
		width: 100%;

		border-radius: var(--brad1);
	}

	.slide {
		display: flex;
		justify-content: center;
		gap: var(--gap1);
		flex-wrap: wrap;

		/* border: 2px solid var(--background); */
		/* padding: var(--gap3); */
	}
	.slide > * {
		display: flex;
		align-items: center;
		justify-content: center;

		--size: 50px;
		width: var(--size);
		height: var(--size);
		cursor: pointer;

		border: 2px solid var(--background);
		border-radius: var(--brad1);

		transition: var(--trans1);
	}
	.slide > *:hover {
		border-color: var(--midtone);
		transform: scale(1.1);
	}
	.slide > *.active {
		border-color: var(--color1);
	}
</style>
