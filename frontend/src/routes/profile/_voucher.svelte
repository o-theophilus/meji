<script>
	import { module, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';

	let code;
	let error;
	let { user } = $module;

	const validate = async () => {
		error = '';

		if (!code) {
			error = 'This field is required';
		} else if (code.length != 10) {
			error = 'invalid code';
		}

		error == '' && submit();
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}user_voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ code })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Voucher Added',
				message: `Your voucher has been added successfully`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
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
	<Button class="primary" name="Add" on:click={validate} />
</Form>
