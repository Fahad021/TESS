/**
 * SLAC 2019
 *
 * Created by: Jonathan G.
 *
 * Application landing page 
 */

import React from 'react'
import { connect } from 'react-redux'
import Button from '../common/components/TessButton'
import { View, Text, StyleSheet } from 'react-native'

/**
 * Landing page component
 * When the application launches and after the user signs out, this is
 * the page that they'll get dumped on.
 */
class LandingPage extends React.Component {
    navigateToLogin = () => {
        this.props.navigation.navigate('SignInSignUpPage', { isSignUp: false })
    }

    navigateToDisclaimer = () => {
        this.props.navigation.navigate('DisclaimerPage')
    }

    render() {
        return (
            <View>
                <View style={styles.logoContainer}>
                    <Text>TESS logo placeholder</Text>
                </View>

                <View style={styles.tessDescriptionContainer}>
                    <Text style={styles.tessDescriptionText}>
                        Share your energy data, advance science, and take part in the value created.
                    </Text>
                    <View style={styles.spacer}/>
                    <Text style={styles.tessDescriptionText}>
                        TESS is secure, private, and free.
                    </Text>
                </View>

                <View style={styles.button}>
                    <Button 
                        title='Join the movement'
                        accessibilityLabel='join the movement'
                        onPress={this.navigateToDisclaimer} />
                </View>

                <View style={styles.loginContainer}>
                    <Text onPress={this.navigateToLogin}>
                        Already a member? <Text style={styles.loginLink}>Login</Text>
                    </Text>
                </View>
            </View>            
        )
    }
}

export default connect()(LandingPage)

const styles = StyleSheet.create({
    loginLink: {
        fontSize: 12,
        color: 'blue',
        textDecorationLine: 'underline',
        textDecorationStyle: 'solid',
    },
    logoContainer: {
        alignItems: 'center',
        marginHorizontal: 15,
        marginTop: 75,
        marginBottom: 45
    },
    tessDescriptionContainer: {
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingVertical: 25,
        marginBottom: 45,
        borderColor: 'black',
        borderWidth: 2
    },
    tessDescriptionText: {
        textAlign: 'center',
        fontSize: 14
    },
    spacer: {
        marginTop: 30
    },
    loginContainer: {
        alignItems: 'center',
        marginTop: 10
    }, 
    button: {
        marginHorizontal: 20
    }
})
