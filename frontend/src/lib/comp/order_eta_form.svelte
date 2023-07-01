<script>
	import { module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';

	export let data;
	let form = data;
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.date) {
			error.date = 'This field is required';
		}

		if (!form.time) {
			error.time = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order_date/${form.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.order);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Set Delivery date and time</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="date"> Date: </label>
			<input type="date" bind:value={form.date} id="date" placeholder="date here" />
			{#if error.date}
				<p class="error">
					{error.date}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="time"> Time: </label>
			<input type="time" bind:value={form.time} id="time" placeholder="time here" />
			{#if error.time}
				<p class="error">
					{error.time}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
