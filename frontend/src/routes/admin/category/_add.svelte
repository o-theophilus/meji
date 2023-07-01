<script>
	import { tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	let form = {};
	let error = '';

	const validate = async () => {
		error = '';

		if (!form.name) {
			error = 'This field is required';
		}

		!error && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category`, {
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
				tick(resp.data.categories);
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Category</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="name"> Name: </label>
			<input type="text" bind:value={form.name} id="name" placeholder="Name here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<label for="icon"> Icon: </label>
			<input type="text" bind:value={form.icon} id="icon" placeholder="Icon here" />
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
