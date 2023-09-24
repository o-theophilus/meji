<script>
	import { module, loading } from '$lib/store.js';

	import Button from '$lib/button.svelte';
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
		$loading = true;
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
	<IG name="name_" label="Fullname" {error} let:id>
		<input bind:value={form.name} {id} type="text" placeholder="Fullname here" />
	</IG>

	<IG name="email_" {error} let:id>
		<input bind:value={form.email} {id} type="email" placeholder="Email here" />
	</IG>

	<IG name="phone" {error} let:id>
		<input bind:value={form.phone} {id} type="tel" placeholder="Phone number here" />
	</IG>

	<IG name="message" {error} let:id>
		<textarea bind:value={form.message} {id} placeholder="Message here" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}

			<br />
		</p>{/if}
	<Button class="primary" on:click={validate}>Submit</Button>
</form>
