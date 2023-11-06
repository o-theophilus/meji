<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Quantity from '$lib/item/quantity.svelte';

	let form = {
		quantity: 1
	};
	let error = {};

	const validate = async () => {
		error = {};

		if (form.value && (!Number.isFinite(form.value) || form.value <= 0)) {
			error.value = 'please enter a valid value';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'creating . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'voucher',
				data: resp.vouchers
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'Voucher added'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Add Voucher</b>
		Add a new Voucher
	</svelte:fragment>

	<IG name="value" {error} bind:value={form.value} type="number" placeholder="Value here" />

	<IG name="quantity" {error} let:id>
		<Quantity
			quantity={1}
			{id}
			on:done={(e) => {
				form.quantity = e.detail.quantity || 1;
			}}
		/>
	</IG>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" on:click={validate}>Create</Button>
</Form>
