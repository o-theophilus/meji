<script>
	import { tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	export let data;
	let error = {};

	const validate = async () => {
		error = {};

		if (!data.name) {
			error.name = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag/${data.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(data)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.tags);
			} else if (resp.status == 201) {
				error.name = resp.message;
			} else {
				error.form = resp.message;
			}
		}
	};

	const del = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag/${data.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.tags);
			} else {
				error.form = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit tag</div>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.form}
			<p class="error">
				{error.form}
			</p>
		{/if}
		<div class="inputGroup">
			<label for="name"> Name: </label>
			<input type="text" bind:value={data.name} id="name" placeholder="Name here" />
			{#if error.name}
				<p class="error">
					{error.name}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<label for="icon"> Icon: </label>
			<input type="text" bind:value={data.icon} id="name" placeholder="Icon here" />
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" on:click={validate} />
			<Button name="Delete" on:click={del} />
		</div>
	</form>
</Form>
