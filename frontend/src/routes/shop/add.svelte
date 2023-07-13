<script>
	import { goto } from '$app/navigation';

	import { module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	let form = {};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.name) {
			error.name = 'This field is required';
		}

		if (!form.price) {
			error.price = 'This field is required';
		} else if (!Number.isInteger(form.price) || form.old_price < 1) {
			error.price = 'Please enter a valid price';
		}

		if (!form.old_price) {
			if (form.old_price == 0) {
				error.old_price = 'Please enter a valid price fe1';
			}
		} else if (
			!/[0-9]/.test(form.old_price) ||
			!Number.isInteger(form.old_price) ||
			form.old_price < 1
		) {
			error.old_price = 'Please enter a valid price fe2';
		} else if (form.price >= form.old_price) {
			error.old_price = 'Old price should be greater than Price';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			if (resp.status == 200) {
				goto(`/${resp.data.item.slug}`);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Item</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		<p>Add a new item</p>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="name"> Name: </label>
			<input type="text" bind:value={form.name} id="name" placeholder="Name here" />
			{#if error.name}
				<p class="error">
					{error.name}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="price"> Price: </label>
			<input type="number" bind:value={form.price} id="price" placeholder="Price here" />
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
				bind:value={form.old_price}
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
			<label for="info"> Description: </label>
			<textarea type="text" bind:value={form.info} id="info" placeholder="Description here" />
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
