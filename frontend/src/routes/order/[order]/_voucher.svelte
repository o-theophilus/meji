<script>
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/module/form.svelte';

	let error = '';
	let value = '';

	const validate = async () => {
		error = '';

		if (!value) {
			error = 'This field is required';
		} else if (value.length != 10) {
			error = 'invalid code';
		}

		error == '' && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user_voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ code: value })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user.acc_balance = resp.data.user.acc_balance;
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Voucher Code</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup horizontal">
			<label for="code"> Voucher Code: </label>
			<input type="text" bind:value id="code" placeholder="Voucher code here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button name="Add" class="primary" />
		</div>
	</form>
</Form>

<style>
</style>
