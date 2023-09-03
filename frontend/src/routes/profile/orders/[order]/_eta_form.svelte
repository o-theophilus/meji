<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let form = {
		key: $module.key,
		date: $module.date,
		time: $module.time
	};
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
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_date/${form.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.order;
			$module = '';
			$toast = {
				status: '200',
				message: 'Arrival time updated'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Set Delivery date and time</b>
	</svelte:fragment>

	<IG name="date" {error} let:id>
		<input bind:value={form.date} {id} type="date" placeholder="date here" />
	</IG>
	<IG name="time" {error} let:id>
		<input bind:value={form.time} {id} type="time" placeholder="time here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" name="Submit" on:click={validate} />
</Form>
