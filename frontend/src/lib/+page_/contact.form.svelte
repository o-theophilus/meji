<script>
	import { module, loading } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/info.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name_ = 'please enter your name';
		}
		if (!form.email) {
			error.email_ = 'please enter your name';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email_ = 'please enter a valid email address';
		}
		if (!form.message) {
			error.message = 'please enter your message';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'sending . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/contact`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module = {
				module: Info,
				status: 200,
				title: 'Message Sent',
				message: 'Thank you for contacting us. We will attend to your message as soon as possible.',
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
			error = resp.error;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<IG
		name="name_"
		label="Full name"
		{error}
		bind:value={form.name}
		type="text"
		placeholder="Full name here"
	/>

	<IG name="email_" {error} bind:value={form.email} type="email" placeholder="Email here" />
	<IG name="phone" {error} bind:value={form.phone} type="tel" placeholder="Phone number here" />
	<IG name="message" {error} bind:value={form.message} type="textarea" placeholder="Message here" />

	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}

	<Button primary on:click={validate}>Send</Button>
</form>
