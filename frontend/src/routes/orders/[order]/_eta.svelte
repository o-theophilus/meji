<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let today = new Date();
	today.setHours(10, 0, 0, 0);
	var year = today.getFullYear();
	var month = (today.getMonth() + 1).toString().padStart(2, '0');
	var day = today.getDate().toString().padStart(2, '0');
	let min = `${year}-${month}-${day}T00:00:00`;

	var year = $module.order.delivery_date.getFullYear();
	var month = ($module.order.delivery_date.getMonth() + 1).toString().padStart(2, '0');
	var day = $module.order.delivery_date.getDate().toString().padStart(2, '0');
	var hours = $module.order.delivery_date.getHours().toString().padStart(2, '0');
	var minutes = $module.order.delivery_date.getMinutes().toString().padStart(2, '0');
	var seconds = $module.order.delivery_date.getSeconds().toString().padStart(2, '0');
	let delivery_date = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
	let error = {};

	const validate = async () => {
		error = {};
		if (!delivery_date) {
			error.date = 'This field is required';
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/eta/${$module.order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ delivery_date })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'order',
				data: resp.order
			};
			$module = '';
			$toast = {
				status: 200,
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

	<IG
		name="date"
		{error}
		bind:value={delivery_date}
		type="datetime"
		{min}
		placeholder="date here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Ok</Button>
</Form>
