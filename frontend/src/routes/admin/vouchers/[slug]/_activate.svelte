<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Number from '$lib/number.svelte';
	import IG from '$lib/input_group.svelte';
	import Datetime from '$lib/datetime.svelte';

	let validity = 2;
	let error = {};

	let date;
	$: {
		date = new Date();
		date.setDate(date.getDate() + validity);
	}

	const submit = async () => {
		$loading = 'activating . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/activate/${$module.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ validity })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				voucher: resp.voucher,
				logs: resp.logs
			};

			$module = '';
			$toast = {
				status: 200,
				message: 'Voucher activated'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Activate Voucher</b>
	</svelte:fragment>

	<IG label="days" name="validity" {error} let:id>
		<Number
			value={validity}
			{id}
			on:change={(e) => {
				validity = e.detail;
			}}
		/>
	</IG>

	Voucher will be valid till:
	<br />
	<Datetime datetime={date} type="date" />
	<br />
	<br />

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" on:click={submit}>Activate</Button>
</Form>

<style>
</style>
