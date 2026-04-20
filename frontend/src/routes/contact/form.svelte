<script>
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { Dropdown, IG } from '$lib/input';
	import { EmailTemplate, Form } from '$lib/layout';
	import { app, loading, module } from '$lib/store.svelte.js';
	import { template } from './form.template.js';

	let email_template;
	let form = $state({});
	let error = $state({});

	$effect(() => {
		const x = page.url.pathname;
		error = {};
	});

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			error.email = 'This field cannot exceed 255 characters';
		}

		if (!form.message) {
			error.message = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Sending Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/contact`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			form = {};

			module.open(Dialogue, {
				title: 'Message Sent',
				message: `
					   Thank you for contacting me,
					   <br/>
					   I will get back to you shortly
					   `,
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							module.close();
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<!-- description="Need help tracking an order, resolving an issue, or making a purchase decision? Our team is ready to assist you.
	<br/>
	<br/>
" -->
<Form title="Get In Touch" error={error.error} --form-padding="0">
	<IG
		name="Full Name"
		icon="user"
		bind:value={form.name}
		error={error.name}
		type="text"
		placeholder="Name Here"
	/>
	<IG
		name="Email Address"
		icon="mail"
		bind:value={form.email}
		error={error.email}
		type="text"
		placeholder="Email here"
	/>
	<IG
		bind:value={form.message}
		error={error.message}
		type="textarea"
		placeholder="Tell us what you need help with (e.g. order issue, payment problem, product question). Include your Order ID if available."
	>
		{#snippet label()}
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft1)"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-outline-color="transparent"
				label="How can we help?"
				value="hidden"
				list={Object.keys(template)}
				icon2="chevron-down"
				onchange={(e) => {
					form.message = template[e];
				}}
			/>
		{/snippet}
	</IG>

	<Button
		--button-background-color="var(--cl1)"
		--button-outline-color="transparent"
		--button-color="hsl(0, 0%, 95%)"
		icon2="send-horizontal"
		onclick={validate}>Contact Support</Button
	>

	<div class="note">We typically respond within a few hours.</div>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate>
		Name: {'{'}name{'}'}
		<br />
		Email: {'{'}email{'}'}
		<br /><br />
		{'{'}message{'}'}
	</EmailTemplate>
</div>

<style>
	.note {
		margin-top: 16px;
		font-size: 0.8rem;
	}
</style>
