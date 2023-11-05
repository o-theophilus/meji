<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let code;
	let error = {};

	const validate = async () => {
		error = {};

		if (!code) {
			error = 'This field is required';
		} else if (code.length != 10) {
			error = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = "adding . . .";
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/use_voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ code })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'user',
				data: resp.user
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'voucher added'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Add Voucher</b>
		Add to your balance.
	</svelte:fragment>

	<IG name="voucher" {error} let:id>
		<input bind:value={code} {id} type="text" placeholder="Your code here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Add</Button>
</Form>
