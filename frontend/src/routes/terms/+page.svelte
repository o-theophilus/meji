<script>
	import Card from '$lib/card.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Center from '$lib/center.svelte';
	import Title from '$lib/title.svelte';

	let md = `
# Terms of use

By using or accessing Meji, you agree to this Statement, as updated from time to time in
accordance with Section 12 below. Additionally, you will find our Privacy Policy at the end of
this document.
	
1. ## Sharing Your Content and Information

	We own all of the content and information you post on Meji.

	1. For content that is covered by intellectual property rights, like photos and videos (IP content), you specifically give us the following permission: you grant us a non-exclusive, transferable, sub-licensable, royalty-free, worldwide license to use any IP content that you post on or in connection with Meji (IP License). This IP License ends when you delete your IP content or your account unless your content has been shared with others, and they have not deleted it.
	1. When you delete IP content, it is deleted in a manner similar to emptying the recycle bin on a computer. However, you understand that removed content may persist in backup copies for a reasonable period of time (but will not be available to others).
	1. When you publish content or information using the Public setting, it means that you are allowing everyone, including people off of Meji, to access and use that information, and to associate it with you (i.e., your name and profile picture).
	1. We always appreciate your feedback or other suggestions about Meji, but you understand that we may use your feedback or suggestions without any obligation to compensate you for them (just as you have no obligation to offer them).

1. ## Safety

	We do our best to keep Meji safe, but we cannot guarantee it. We need your help to keep
	Meji safe, which includes the following commitments by you:

	1. You will not post unauthorized commercial communications (such as spam) on Meji
	1. You will not stoect users' content or information, or otherwise access Meji, using automated means (such as harvesting bots, robots, spiders, or scrapers) without our prior permission.
	1. You will not engage in unlawful multi-level marketing, such as a pyramid scheme, on Meji.
	1. You will not upload viruses or other malicious code.
	1. You will not solicit login information or access an account belonging to someone else.
	1. You will not bully, intimidate, or harass any user.
	1. You will not post content that: is hate speech, threatening, or pornographic; incites violence; or contains nudity or graphic or gratuitous violence.
	1. You will not develop or operate a third-party application containing alcohol-related, dating or other mature content (including advertisements) without appropriate age-based restrictions.
	1. You will not use Meji to do anything unlawful, misleading, malicious, or discriminatory.
	1. You will not do anything that could disable, overburden, or impair the proper working or appearance of Meji, such as a denial of service attack or interference with page rendering or other Meji functionality.
	1. You will not facilitate or encourage any violations of this Statement or our policies.
	
1. ## Registration and Account Security

	Meji users provide their real names and information, and we need your help to keep it
	that way. Here are some commitments you make to us relating to registering and maintaining
	the security of your account:
	1. You will not provide any false personal information on Meji, or create an account for anyone other than yourself without permission.
	
	1. You will not create more than one personal account.
	1. If we disable your account, you will not create another one without our permission.
	1. You will not use Meji if you are under 13.
	1. You will keep your contact information accurate and up-to-date.
	1. You will not share your password , let anyone else access your account, or do anything else that might jeopardize the security of your account.
	1. You will not transfer your account to anyone without first getting our written permission.
	1. If you select a username or similar identifier for your account, we reserve the right to remove or reclaim it if we believe it is appropriate (such as when a trademark owner complains about a username that does not closely relate to a user's actual name).
	
	
1. ## Amendments
    1. We'll notify you before we make changes to these terms and give you the opportunity to review and comment on the revised terms before continuing to use our Services.
    1. If we make changes to policies, guidelines or other terms referenced in or incorporated by this terms of service, we may provide notice on the Site Governance Page.
    1. Your continued use of Meji, following notice of the changes to our terms, policies or guidelines, constitutes your acceptance of our amended terms, policies or guidelines.
			
	
1. ## Termination
	
    If you violate the letter or spirit of this terms of service, or otherwise create risk or
    possible legal exposure for us, we can stop providing all or part of Meji to you. We will
    notify you by email or at the next time you attempt to access your account. You may also
    delete your account or disable your application at any time. In all such cases, this
    Statement shall terminate, but the following provisions will still apply: 2.2, 2.4, 3-5,
    9.3, and 14-18.

1. ## Disputes
	
    1. You will resolve any claim, cause of action or dispute (claim) you have with us arising out of or relating to this terms of service or Meji exclusively in a Lagos, Nigeria court, and you agree to submit to the personal jurisdiction of such courts for the purpose of litigating all such claims. The laws of the State of Lagos will govern this Statement, as well as any claim that might arise between you and us, without regard to conflict of law provisions.
	1. If anyone brings a claim against us related to your actions, content or information on Meji, you will indemnify and hold us harmless from and against all damages, losses, and expenses of any kind (including reasonable legal fees and costs) related to such claim. Although we provide rules for user conduct, we do not control or direct users' actions on Meji and are not responsible for the content or information users transmit or share on Meji. We are not responsible for any offensive, inappropriate, obscene, unlawful or otherwise objectionable content or information you may encounter on Meji. We are not responsible for the conduct, whether online or offline, of any user of Meji.
	1. WE TRY TO KEEP Meji BUG-FREE, AND SAFE, BUT YOU USE IT AT YOUR OWN RISK. WE ARE PROVIDING Meji AS IS WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WE DO NOT GUARANTEE THAT Meji WILL ALWAYS BE SAFE, SECURE OR ERROR-FREE OR THAT Meji WILL ALWAYS FUNCTION WITHOUT DISRUPTIONS, DELAYS OR IMPERFECTIONS. Meji IS NOT RESPONSIBLE FOR THE ACTIONS, CONTENT, INFORMATION, OR DATA OF THIRD PARTIES, AND YOU RELEASE US, OUR DIRECTORS, OFFICERS, EMPLOYEES, AND AGENTS FROM ANY CLAIMS AND DAMAGES, KNOWN AND UNKNOWN, ARISING OUT OF OR IN ANY WAY CONNECTED WITH ANY CLAIM YOU HAVE AGAINST ANY SUCH THIRD PARTIES. AS A USER OF Meji, YOU WAIVE ANY CIVIL CODE, WHICH SAYS: A GENERAL RELEASE DOES NOT EXTEND TO CLAIMS WHICH THE CREDITOR DOES NOT KNOW OR SUSPECT TO EXIST IN HIS OR HER FAVOR AT THE TIME OF EXECUTING THE RELEASE, WHICH IF KNOWN BY HIM OR HER MUST HAVE MATERIALLY AFFECTED HIS OR HER SETTLEMENT WITH THE DEBTOR. WE WILL NOT BE LIABLE TO YOU FOR ANY LOST PROFITS OR OTHER CONSEQUENTIAL, SPECIAL, INDIRECT, OR INCIDENTAL DAMAGES ARISING OUT OF OR IN CONNECTION WITH THIS TERMS OF SERVICE OR Meji, EVEN IF WE HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. OUR AGGREGATE LIABILITY ARISING OUT OF THIS TERMS OF SERVICE OR Meji WILL NOT EXCEED THE GREATER OF ONE HUNDRED DOLLARS ($100) OR THE AMOUNT YOU HAVE PAID US IN THE PAST TWELVE MONTHS. APPLICABLE LAW MAY NOT ALLOW THE LIMITATION OR EXCLUSION OF LIABILITY OR INCIDENTAL OR CONSEQUENTIAL DAMAGES, SO THE ABOVE LIMITATION OR EXCLUSION MAY NOT APPLY TO YOU. IN SUCH CASES, Meji'S LIABILITY WILL BE LIMITED TO THE FULLEST EXTENT PERMITTED BY APPLICABLE LAW.

1. ## Disputes

    We strive to create a global community with consistent standards for everyone, but we also strive to respect local laws. The following provisions apply to users and non-users who interact with Meji outside the United States and Nigeria:
	
    1. You consent to having your personal data transferred to and processed in the United States and Nige 1. If you are located in a country embargoed by the United States, or are on the U.S. Treasury Department's list of Specially Designated Nati you will not engage in commercial activities on Meji (such as advertising or payments) or operate a Platform application or website. You will not use Meji if you are prohibited from receiving products, services, or software originating from the United States
	
	
1. ## Definitions

    1. By "Meji" we mean the features and services we make available, including through (a) our website at www.Meji.ng and any other Meji branded or co-branded websites (including sub-domains, international versions, widgets, and mobile versions); (b) social plugins such as the the Share button and other similar offerings; and (c) other media, brands, products, services, software (such as a toolbar), devices, or networks now existing or later developed. Meji reserves the right to designate, in its sole discretion, that certain of our brands, products, or services are governed by separate terms and not this terms of service.
	1. By "information" we mean facts and other information about you, including actions taken by users and non-users who interact with Meji.
	1. By "content" we mean anything you or other users post, provide or share using Meji.
	1. By "data" or "user data" or "user's data" we mean any data, including a user's content or information that you or third parties can retrieve from Meji or provide to Meji.
    1. By "post" we mean post on Meji or otherwise make available by using Meji.
	1. By "use" we mean use, run, copy, publicly perform or display, distribute, modify, translate, and create derivative works of.
	1. By “Trademarks” we mean the Meji trademarks.
	
1. ## Other
	1. This Statement is an agreement between you and Meji Nigeria Limited. References to “us,” “we,” and “our” mean Meji Nigeria Limited, as appropriate.
	1. This terms of service makes up the entire agreement between the parties regarding Meji, and supersedes any prior agreements.
	1. If any portion of this terms of service is found to be unenforceable, the remaining portion will remain in full force and effect.
	1. If we fail to enforce any of this terms of service, it will not be considered a waiver.
	1. Any amendment to or waiver of this terms of service must be made in writing and signed by us.
	1. You will not transfer any of your rights or obligations under this terms of service to anyone else without our consent.
	1. All of our rights and obligations under this terms of service are freely assignable by us in connection with a merger, acquisition, or sale of assets, or by operation of law or otherwise.
	1. Nothing in this terms of service shall prevent us from complying with the law
	1. This terms of service does not confer any third party beneficiary rights
	1. We reserve all rights not expressly granted to you
	1. You will comply with all applicable laws when using or accessing Meji

**By using or accessing Meji, you agree that we can stoect and use such content and information in accordance with the Privacy policy as amended from time to time.** 

To access the terms of service in several different languages, change the language setting for your Meji session by clicking on the language link in the left corner of most pages. If the terms of service is not available in the language you select, we will default to the English version
	
*Effective: March 24, 2019*


# Privacy Policy
This policy describes what information we stoect and how it is used and shared.

## What kinds of information do we stoect?
We stoect different kinds of information from or about you.

## Things you do and information you provide.
We stoect the content and other information you provide when you use Meji, including when
you sign up for an account, create or share, and message or communicate with others. This can
include information in or about the content you provide, such as the location of a photo or
the date a file was created. We also stoect information about how you use Meji, such as the
types of content you view or engage with or the frequency and duration of your activities.
		

## Things others do and information they provide.
We also stoect content and information that other people provide when they use Meji,
including information about you, such as when they share a photo of you, send a message to
you, or upload, sync or import your contact information.
		

## Information from third-party partners.
We receive information about you and your activities on and off Meji from third-party
partners, such as information from a partner when we jointly offer services or from an
advertiser about your experiences or interactions with them.
		

## How do we use this information?
We are passionate about creating engaging and customized experiences for people. We use all of
the information we have to help us provide and support Meji. Here’s how:
		

## Provide, improve and develop Services.
We are able to deliver our Services, personalize content, and make suggestions for you by
using this information to understand how you use and interact with our Services and the people
or things you’re connected to and interested in on and off our Services.

We also use information we have to provide shortcuts and suggestions to you. For example, we are
able to suggest that your friend tag you in a picture by comparing your friend's pictures to information
we've put together from your profile pictures and the other photos in which you've been tagged.
If this feature is enabled for you, you can control whether we suggest that another user tag you
in a photo using the “Timeline and Tagging” settings.

When we have location information, we use it to tailor our Services for you and others, like helping
you to check-in and find local information or offers in your area.

We conduct surveys and research, test features in development, and analyze the information we have
to evaluate and improve products and services, develop new products or features, and conduct audits
and troubleshooting activities.
		

## Communicate with you.
We use your information to send you marketing communications, communicate with you about our
Services and let you know about our policies and terms. We also use your information to
respond to you when you contact us.
		

## Show and measure ads and services.
We use the information we have to improve our advertising and measurement systems so we can
show you relevant ads on and off our Services and measure the effectiveness and reach of ads
and services.
		

## Promote safety and security.
We use the information we have to help verify accounts and activity, and to promote safety and
security on and off of our Service, such as by investigating suspicious activity or violations
of our terms or policies. We also offer easy-to-use security tools that add an extra layer of
security to your account. We use cookies and similar technologies to provide and support our
Services and each of the uses outlined and described in this section of our policy.
		

## Sharing With Third-Party Partners and Customers
We work with third party companies who help us provide and improve our Services or who use
advertising or related products, which makes it possible to operate our companies and provide
free services to people around the world.
		
## Vendors, service providers and other partners.
We transfer information to vendors, service providers, and other partners who globally support
our business, such as providing technical infrastructure services, analyzing how our Services
are used, measuring the effectiveness of ads and services, providing customer service,
facilitating payments, or conducting academic research and surveys. These partners must adhere
to strict confidentiality obligations in a way that is consistent with this Privacy Policy and
the agreements we enter into with them.
		
## How can I manage or delete information about me?
We store data for as long as it is necessary to provide products and services to you and
others, including those described above. Information associated with your account will be kept
until your account is deleted, unless we no longer need the data to provide products and
services.

You can delete your account any time. When you delete your account, we delete things you have posted,
such as your photos and status updates. If you do not want to delete your account, but want to
temporarily stop using Meji, you may deactivate your account instead. To learn more about deactivating
or deleting your account. Keep in mind that information that others have shared about you is not
part of your account and will not be deleted when you delete your account.
		
## How will we notify you of changes to this policy?
We'll notify you before we make changes to this policy and give you the opportunity to review
and comment on the revised policy before continuing to use our Services.
		
## How to contact Meji with questions
Contact Us: [Contact](/#contact)
	`;
</script>

<Meta title="Terms and Conditions" description="Terms and Conditions" />
<Log entity_type={'page'} />

<Center>
	<Title>Terms and Conditions</Title>
</Center>

<Card>
	<Marked {md} />
</Card>
