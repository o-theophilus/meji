<script>
	import { module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	export let data;
	let { item } = data;

	item.old_price = item.old_price ? item.old_price : undefined;
	let error = {};

	const validate = async () => {
		error = {};

		if (!item.name) {
			error.name = 'This field is required';
		}
		if (!item.price) {
			error.price = 'This field is required';
		} else if (!Number.isInteger(item.price) || item.price < 1) {
			error.price = 'Please enter a valid price';
		}

		if (!item.old_price) {
			if (item.old_price == 0) {
				error.old_price = 'Please enter a valid price fe1';
			}
		} else if (
			!/[0-9]/.test(item.old_price) ||
			!Number.isInteger(item.old_price) ||
			item.old_price < 1
		) {
			error.old_price = 'Please enter a valid price fe2';
		} else if (item.price >= item.old_price) {
			error.old_price = 'Old price should be greater than Price';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = '';

				let { alias } = resp.data.item;
				if (item.alias != alias) {
					window.history.replaceState('', '', `/${alias}`);
				}
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Item</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="name"> Name: </label>
			<input type="text" bind:value={item.name} id="name" placeholder="Name here" />
			{#if error.name}
				<p class="error">
					{error.name}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="price"> Price: </label>
			<input type="number" bind:value={item.price} id="price" placeholder="Price here" />
			{#if error.price}
				<p class="error">
					{error.price}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="old_price"> Old Price: </label>
			<input
				type="number"
				bind:value={item.old_price}
				id="old_price"
				placeholder="Old Price here"
			/>
			{#if error.old_price}
				<p class="error">
					{error.old_price}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="desc"> Description: </label>
			<textarea type="text" bind:value={item.desc} id="desc" placeholder="Description here" />
		</div>

		<div class="inputGroup">
			<label for="spec"> Specification: </label>
			<textarea type="text" bind:value={item.spec} id="spec" placeholder="Specification here" />
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
