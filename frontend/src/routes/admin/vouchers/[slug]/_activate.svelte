<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let today = new Date();
	today.setHours(0, 0, 0, 0);
	let t30 = new Date(today);
	t30.setDate(today.getDate() + 30);
	let validity = t30.toISOString().split('T')[0];

	$: to = new Date(form.validity);
	$: difference = Math.ceil((to - today) / (1000 * 60 * 60 * 24));
	let min = today.toISOString().split('T')[0];

	let form = {
		validity: validity
	};
	let voucher = { ...$module.voucher };
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.validity) {
			error.validity = 'this field is required';
		} else if (new Date(form.validity) < today) {
			error.validity = 'cannot be back dated';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/activate_voucher/${voucher.key}`, {
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
			$portal = resp.voucher;
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
		<b>Activate coucher</b>
	</svelte:fragment>

	<IG name="validity" {error} let:id>
		<input bind:value={form.validity} {id} type="date" {min} placeholder="date here" />
		{difference} day{difference > 1 ? 's' : ''}
	</IG>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" on:click={validate}>Submit</Button>
</Form>
